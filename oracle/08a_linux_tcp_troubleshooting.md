# 08a. Linux, TCP, and production troubleshooting

Questions 1–9 and 28–32 from the OCI loop, plus the follow-ups that sit on the same path: handshake, state machine, listen backlog, socket exhaustion, and the commands.

<div class="callout note">
<b>How to answer this drill.</b> Name the errno or the state first, then the side that sent the segment, then the command that proves it. TIME_WAIT, CLOSE_WAIT, and FIN_WAIT are <b>states</b>, not TCP flags. The flags that move the state machine are SYN, ACK, FIN, and RST.
</div>

---

## Definitions you need before question 1

| Term | Meaning |
|---|---|
| **Socket** | The kernel object for one endpoint of a communication channel. A TCP socket is identified by the 4-tuple `(local IP, local port, remote IP, remote port)`. A listening socket is `(local IP, local port, *, *)`. |
| **Bind** | Assign a local address and port to a socket (`bind()`). This happens **before** `listen()`. It does not send any packets. |
| **Listen** | Mark the socket passive and create the accept queue (`listen(fd, backlog)`). |
| **Port** | A 16-bit number, 0–65535. Ports **0–1023** are privileged (well-known). |
| **errno** | The integer the kernel returns on failure. The message (`Address already in use`) is just `strerror`. Always ask which errno. |
| **File descriptor (fd)** | An integer index into the process's open-file table. Sockets, files, and pipes all consume fds. |
| **netns** | Network namespace. Containers have their own interfaces, routes, and port space. "Port free on the host" does not mean "port free in the pod." |
| **MSS / MTU** | Maximum segment size / maximum transmission unit. Not the cause of a bind failure. Relevant later for latency and black holes. |
| **MSL** | Maximum segment lifetime. The longest a segment is assumed to live in the network. TCP uses **2×MSL** (commonly 60s, so TIME_WAIT is often 60s; Linux `tcp_fin_timeout` is a different timer). |

**Assumptions to say out loud:** IPv4 or IPv6, TCP not UDP, the process is the one calling `bind` (not a sidecar), and you can get the errno and the command line.

---

## Q1. A process cannot bind to a port. What would you check?

**What they are testing:** a checklist ordered by likelihood, tied to errno, not a random list of tools.

**The answer**

I ask for the errno first. `bind()` fails locally. No peer is involved. The usual causes, in the order I check them:

1. **`EADDRINUSE` — something is already bound.** Another process, a previous instance that didn't die, or systemd socket activation. Check listeners, not all sockets:

```bash
ss -lptn 'sport = :8080'
# or, if ss is missing:
lsof -nP -iTCP:8080 -sTCP:LISTEN
```

   A socket in `TIME_WAIT` is **not** a listener. It rarely blocks `bind` of a **new server** that uses `SO_REUSEADDR` (the default in most servers). It blocks `bind` when you also try to reuse the full 4-tuple, which is a client problem more than a server problem. See Q3.

2. **`EACCES` — privilege.** Port < 1024 and the process is not root and does not have `CAP_NET_BIND_SERVICE`. See Q2.

3. **`EADDRNOTAVAIL` — that IP is not local.** The config says `bind 10.0.0.5` but the interface has a different address, or the address moved after a failover. Check `ip -4 addr`.

4. **IPv4/IPv6 clash.** Binding `::` with `IPV6_V6ONLY=0` also claims the IPv4 port. A second process binding `0.0.0.0:8080` gets `EADDRINUSE`. Check both families:

```bash
ss -lptn | awk '$4 ~ /:8080$/'
sysctl net.ipv6.bindv6only
```

5. **Wrong network namespace.** The port is free in the host netns and taken inside the container, or the process is in a netns that has no interface. `ip netns`, `nsenter -t PID -n ss -lptn`, or `ls -l /proc/PID/ns/net`.

6. **Mandatory access control.** SELinux or AppArmor can deny `bind` even when the port is free. errno is often `EACCES`. `ausearch -m avc -ts recent` or `dmesg`, and `aa-status`.

7. **UNIX socket, not TCP.** If the "port" is a filesystem path (`/var/run/app.sock`), failure is directory permissions, a leftover inode, or the path length. `ls -l` on the socket and its directory. This is not a TCP problem.

8. **Config, not the kernel.** The process is binding a different port than the one you are probing (env var vs flag). Read `/proc/PID/cmdline` and the logs for the address it actually passed to `bind`.

**What I do not check first:** firewall rules. `iptables` / security lists drop **packets**. They do not make `bind()` fail. A firewall explains "clients cannot connect," not "bind failed."

```
bind() failure
   |
   +-- EADDRINUSE ---- ss -lptn sport=:PORT  (LISTEN, both v4 and v6)
   +-- EACCES -------- port < 1024? caps? SELinux?
   +-- EADDRNOTAVAIL - ip addr, is that IP on this host / netns?
   +-- other --------- netns, leftover unix socket, wrong binary/config
```

---

## Q2. What permissions can prevent a bind? How do you check them?

**Definitions**

- **Privileged port:** 0–1023. Historically only root could bind them, so a remote client can trust that "this is really SSH" and not a user process.
- **Capability:** a slice of root. `CAP_NET_BIND_SERVICE` allows bind on privileged ports without full root. Capabilities live on the thread (`CapEff` = effective) and can be on the file (`setcap`).
- **`net.ipv4.ip_unprivileged_port_start`:** Linux sysctl. Ports **at or above** this value are unprivileged. Default is 1024. If an admin set it to 0, every port is unprivileged. If they set it to 8080, then 8080 itself is still privileged.
- **SELinux / AppArmor:** policy can deny the `name_bind` permission even for port 8080.
- **Filesystem DAC** applies to UNIX-domain sockets, not to TCP port numbers.

**The answer**

Three permission layers:

1. **UID / capability for ports below `ip_unprivileged_port_start`.**

```bash
sysctl net.ipv4.ip_unprivileged_port_start
id                      # uid, groups
grep CapEff /proc/PID/status
capsh --decode=$(awk '/CapEff/ {print $2}' /proc/PID/status)
getcap $(readlink -f /proc/PID/exe)    # file capability on the binary
```

   `cap_net_bind_service` in `CapEff` is what matters at runtime. A file capability does nothing if the process dropped it, or if a container runtime cleared the bounding set. In OCI / Docker, the default capability set often **includes** `NET_BIND_SERVICE`, but a hardened container drops it. Then port 443 fails with `EACCES` even though the image "works on my laptop as root."

2. **MAC.**

```bash
ps -eZ | grep PID          # SELinux context
ausearch -m avc -ts recent | grep -i bind
aa-status                  # AppArmor
```

3. **UNIX socket path mode.** `stat` the directory. The process needs write+execute on the directory to `bind()` a pathname socket.

**Related: how a service should bind 443 without running as root.** Bind the privileged port as root (or via systemd socket activation, or `setcap cap_net_bind_service=+ep`), then `setuid` to an unprivileged user. systemd `User=` plus `AmbientCapabilities=CAP_NET_BIND_SERVICE` is the modern form. Do not leave the whole process as root just to bind a port.

### Likely follow-up: `SO_REUSEADDR` vs `SO_REUSEPORT`

| Option | What it allows |
|---|---|
| **`SO_REUSEADDR`** | Bind a port that still has `TIME_WAIT` sockets from an old 4-tuple. Also lets a new listener start after a crash. It does **not** let two listeners share the port. |
| **`SO_REUSEPORT`** | Multiple sockets (usually multiple processes) bind the **same** IP and port. The kernel distributes new connections. Each socket needs the option set. Used for multi-process servers so they don't share one accept queue. |

`SO_REUSEADDR` does not fix `EACCES`. It fixes a narrow `EADDRINUSE`.

### Likely follow-up: `EADDRINUSE` on a client, not a server

Outbound connections use an **ephemeral port**. The client 4-tuple must be unique. If every ephemeral port to one destination is stuck in `TIME_WAIT`, `connect()` returns `EADDRINUSE`. Check:

```bash
sysctl net.ipv4.ip_local_port_range
ss -tan state time-wait | awk '{print $4}' | wc -l
```

Range default is often `32768–60999` (~28k ports) **per destination IP**. A client opening and closing connections faster than 2×MSL exhausts it. Fixes: connection pooling (reuse TCP), `tcp_tw_reuse` (safe only for **outbound**, and only when timestamps are on), more source IPs, or HTTP keep-alive. Do not "fix" this by killing `TIME_WAIT`. That state is protecting you from old segments.

---

## Q3. TIME_WAIT vs CLOSE_WAIT vs FIN_WAIT

**Definitions**

TCP close is a **four-way** handshake because each direction has its own stream. Either side can close its direction independently (half-close).

- **Active closer:** the side whose application calls `close()` / `shutdown(SHUT_WR)` **first**. It sends the first FIN.
- **Passive closer:** the side that receives that FIN first.

| State | Who is in it | What is true | Healthy? |
|---|---|---|---|
| **FIN_WAIT_1** | Active closer | We have **sent FIN**. Waiting for ACK of that FIN. | Brief. A pile of them means our FINs are not being ACKed (loss, or peer is gone). |
| **FIN_WAIT_2** | Active closer | Our FIN is **ACKed**. Waiting for the peer's FIN. | Brief, unless the peer half-closes and keeps its write side open. Linux will time this out (`tcp_fin_timeout`, default 60s) if the socket was fully closed. |
| **CLOSE_WAIT** | Passive closer | We have **received** the peer's FIN and ACKed it. **Our application has not called `close()` yet.** The read side is done (EOF). The write side is still open. | A **growing** CLOSE_WAIT count is an application bug: we leak sockets. The kernel will not leave this state until the app closes. |
| **TIME_WAIT** | Active closer, after the full handshake | We have seen the peer's FIN and sent the **final ACK**. We wait 2×MSL so (1) we can retransmit that ACK if it was lost, and (2) stray segments from this 4-tuple cannot be accepted by a new connection. | Normal on the side that closes first. A large count on a **client** can exhaust ephemeral ports. A large count on a **server** usually means the server is the active closer (it closes first) and churn is high. That is often fine. |
| **LAST_ACK** | Passive closer | App has closed, we sent our FIN, waiting for the final ACK. | Brief. |
| **CLOSING** | Both sides sent FIN at the same time | We sent FIN, and we received the peer's FIN before ACK of ours. | Rare. Simultaneous close. |

**The one-line version they want**

- **CLOSE_WAIT:** the **other side** closed, and **we have not**. Bug if it sticks.
- **FIN_WAIT:** **we** closed, and we are waiting for them to finish the handshake.
- **TIME_WAIT:** **we** closed first, the handshake is done, and we are holding the 4-tuple for 2×MSL on purpose.

```
Who called close() first?
        |
        +-- we did ---- FIN_WAIT_1 --> FIN_WAIT_2 --> TIME_WAIT --> CLOSED
        |
        +-- they did -- CLOSE_WAIT --> (app close) --> LAST_ACK --> CLOSED
```

---

## Q4. What TCP flags indicate TIME_WAIT, CLOSE_WAIT, and FIN_WAIT?

**What they are testing:** whether you confuse states with flags. This was the "technically" follow-up.

**The answer**

No flag means "this socket is in TIME_WAIT." Flags are bits on a **segment**. States are memory in the **kernel** for a TCB (transmission control block). `ss` prints the state. `tcpdump` prints flags.

The flags that **cause** the transitions:

| State you enter | Segment that causes it | Flags |
|---|---|---|
| **FIN_WAIT_1** | **Local** stack sends FIN after the app closes. Not something we receive. | outbound `FIN` + `ACK` (FIN piggybacks on an ACK of data already seen) |
| **CLOSE_WAIT** | We **receive** the peer's FIN | inbound `FIN` (almost always `FIN+ACK`). We then **send** `ACK`. |
| **FIN_WAIT_2** | We **receive** ACK of our FIN | inbound `ACK` |
| **TIME_WAIT** | We **receive** the peer's FIN while in FIN_WAIT_2, and we send the final ACK | inbound `FIN+ACK`, outbound `ACK` |
| any → **CLOSED** immediately | **RST** | `RST` aborts. No TIME_WAIT. |

Header bits (the ones to name):

| Flag | Bit meaning |
|---|---|
| **SYN** | Synchronize sequence numbers. Handshake only. |
| **ACK** | Acknowledgment field is valid. Set on almost every segment after the first SYN. |
| **FIN** | Sender is done sending. One direction is closed. Consumes one sequence number. |
| **RST** | Abort. No graceful close. |
| **PSH** | Push buffered data up to the app. Not part of close. |
| **URG** | Urgent pointer. Ignore in this interview unless asked. |

So the precise sentence is: **FIN and ACK move you through close. RST skips it. The state name is not a flag.**

---

## Q5. When does a connection enter CLOSE_WAIT? What does the peer send?

**Answer**

The connection enters **CLOSE_WAIT** on **our** host when the **peer sends a FIN** (the peer's application closed its write side) and our kernel has ACKed it.

```
peer app                peer TCP                 our TCP                 our app
   | close()               |                        |                       |
   |---------------------->| FIN,ACK  seq=X         |                       |
   |                       |----------------------->|                       |
   |                       |                        | ACK seq=X+1           |
   |                       |<-----------------------|                       |
   |                       |                        | state = CLOSE_WAIT    |
   |                       |                        | read() returns 0 (EOF)|
   |                       |                        |---------------------->|
   |                       |                        |                       |
   |                       |                        |  ... until we close() |
   |                       |                        |  we stay in CLOSE_WAIT|
```

**Assumptions:** the socket was `ESTABLISHED`. A FIN from a host we have no TCB for gets a RST, not CLOSE_WAIT.

**What the peer sent:** a segment with **FIN set**. The ACK bit is usually also set, because the peer is still acknowledging our data. The FIN occupies one sequence number, so the ACK we return is `their_seq + 1`.

**Why it stays there:** CLOSE_WAIT means "I know they are done sending. I have not said I am done." The kernel is waiting for **our process** to `close()` or `shutdown(SHUT_WR)`, which sends our FIN and moves the socket to `LAST_ACK`. If the process leaks the fd (forgot `close`, a request handler returned without releasing the connection, a reference cycle in a connection pool), CLOSE_WAIT grows until the process hits its fd limit. That matches a production symptom in Q28–Q32.

**How you see it**

```bash
ss -tanp state close-wait
# Recv-Q on a CLOSE_WAIT socket is unread data. The bug is still the missing close().
```

---

## Q6. When does a connection enter FIN_WAIT? What does your server send?

**Answer**

There are two states. Don't collapse them.

**FIN_WAIT_1.** Our application calls `close()` or `shutdown(SHUT_WR)` while we are `ESTABLISHED` (or `CLOSE_WAIT`, but that goes to `LAST_ACK`, not FIN_WAIT). The **server sends FIN** (typically `FIN+ACK`). We are now the active closer.

**FIN_WAIT_2.** The peer ACKs that FIN. We have sent our last byte. We are waiting for the peer to send **its** FIN.

```
our app                 our TCP                  peer TCP
  | close()               |                        |
  |---------------------->| FIN,ACK                |
  |                       |----------------------->|
  |                       | state = FIN_WAIT_1     |
  |                       |        ACK             |
  |                       |<-----------------------|
  |                       | state = FIN_WAIT_2     |
  |                       |        FIN,ACK         |
  |                       |<-----------------------|
  |                       | ACK                    |
  |                       |----------------------->|
  |                       | state = TIME_WAIT      |
```

**What the server sends to enter FIN_WAIT_1:** a segment with the **FIN** flag. It does not enter FIN_WAIT because it received something. It enters FIN_WAIT because **it** sent FIN.

If they say "FIN_WAIT" without a number, answer both, and say FIN_WAIT_1 is "FIN is on the wire," FIN_WAIT_2 is "FIN is acknowledged, their FIN has not arrived."

---

## Q7. TCP connection-closing flow with FIN and ACK

**Assumptions:** normal active close by the client, no data left unsent, no loss, no simultaneous close. Sequence numbers are simplified.

```
 client (active)                         server (passive)
 ESTABLISHED                             ESTABLISHED

      FIN, ACK   seq=100
      ---------------------------------->
 FIN_WAIT_1
                                         ACK        ack=101
      <----------------------------------
 FIN_WAIT_2                              CLOSE_WAIT
                                         (server app must close)
                                         FIN, ACK   seq=500
      <----------------------------------
                                         LAST_ACK
      ACK        ack=501
      ---------------------------------->
 TIME_WAIT (2 x MSL)                     CLOSED
 CLOSED
```

**Why four segments, not two.** Each direction closes independently. The ACK of the first FIN only means "I received your FIN." It does not mean "I am done sending." The server can still send data after it ACKs the client's FIN (half-close). Only the server's own FIN ends its direction.

**Loss, because they will ask:**

- If the **final ACK** is lost, the server retransmits its FIN (it is in `LAST_ACK`). The client is still in `TIME_WAIT` and resends the ACK. That is the reason TIME_WAIT exists.
- If the client's **first FIN** is lost, the client retransmits it and stays in `FIN_WAIT_1`.
- **RST** anywhere aborts both sides. No TIME_WAIT. You see this when a process dies hard, or when a packet arrives for a port with no socket, or when `tcp_abort_on_overflow` is set.

**Simultaneous close** (both call `close()` before either sees a FIN):

```
 both ESTABLISHED
 both send FIN
 both enter FIN_WAIT_1
 both receive FIN before ACK -> CLOSING
 both receive ACK -> TIME_WAIT
```

### Likely follow-up: full state machine including the handshake

```
 CLOSED
   |  connect()                         |  bind()+listen()
   |  send SYN                          |  passive open
   v                                    v
 SYN_SENT                             LISTEN
   |  recv SYN+ACK                     |  recv SYN, send SYN+ACK
   |  send ACK                         v
   |                              SYN_RCVD
   v                                    |  recv ACK
 ESTABLISHED <--------------------------+
   |
   |  close() sends FIN          recv FIN, send ACK
   v                                    v
 FIN_WAIT_1                        CLOSE_WAIT
   |  recv ACK of FIN                  |  app close() sends FIN
   v                                    v
 FIN_WAIT_2                         LAST_ACK
   |  recv FIN, send ACK               |  recv ACK
   v                                    v
 TIME_WAIT                           CLOSED
   |  2MSL
   v
 CLOSED
```

**Handshake flags**

1. Client → server: `SYN`, seq=J
2. Server → client: `SYN+ACK`, seq=K, ack=J+1
3. Client → server: `ACK`, ack=K+1

After step 3 the connection is **established**. It sits in the **accept queue** until the server calls `accept()`. The handshake does not require `accept()` to complete. That is Q8.

### Likely follow-up: `tcpdump` one-liners

```bash
tcpdump -ni any -tttt "tcp port 8080 and (tcp[tcpflags] & (tcp-fin|tcp-syn|tcp-rst) != 0)"
```

You should be able to point at a line and say "that FIN moved the client to FIN_WAIT_1 and the server toward CLOSE_WAIT."

---

## Q8. SYN backlog vs accept queue

**Definitions**

Linux has **two** queues for a listening socket. People say "the backlog" and mean one of them. Split them.

| Queue | Also called | Who is in it | Kernel structure | Size |
|---|---|---|---|---|
| **SYN backlog** | request socket queue, incomplete connection queue | Handshake **not** finished. SYN received, SYN-ACK sent, final ACK not seen. | `request_sock` | `tcp_max_syn_backlog` (default often 128, 1024, or 4096). Also capped with the listen backlog in modern kernels. |
| **Accept queue** | completed connection queue | Handshake **finished**. Waiting for the application to `accept()`. | full socket, may already hold data | `min(somaxconn, backlog argument to listen())`. `somaxconn` default was 128 for years; many distros now set 4096. The app's `listen(fd, N)` cannot exceed `somaxconn`. |

```
 client                kernel listener                      application
   | SYN                 |                                    |
   |-------------------->|  [ SYN backlog ]                   |
   |<--------------------|  SYN-ACK                           |
   | ACK                 |                                    |
   |-------------------->|  handshake done                    |
   |                     |  move to [ accept queue ]          |
   |                     |                                    | accept()
   |                     |----------------------------------->| new fd
   | data ...            |                                    |
```

**`ss` on a LISTEN socket is backwards from what people guess.** For a socket in state `LISTEN`:

- **Recv-Q** = current **accept queue** depth (completed, not yet accepted).
- **Send-Q** = the **max** accept queue (the backlog).

```bash
ss -lnt
# State  Recv-Q  Send-Q  Local Address:Port
# LISTEN  0       4096    0.0.0.0:8080
# Recv-Q climbing toward Send-Q  => app is not accepting fast enough

sysctl net.core.somaxconn
sysctl net.ipv4.tcp_max_syn_backlog
sysctl net.ipv4.tcp_abort_on_overflow
sysctl net.ipv4.tcp_syncookies
```

The application's listen backlog is in `/proc/PID/net/tcp` or, easier, in the server's config (`backlog` in Go's `net.Listen`, nginx `backlog=`, Python `socket.listen`). Go's default listen backlog is `somaxconn`.

---

## Q9. What happens to a connection in each queue?

**SYN backlog**

- Kernel has **no file descriptor** for the application. The app cannot read this connection.
- Kernel retransmits SYN-ACK (`tcp_synack_retries`, often 5, over tens of seconds) until the client's ACK arrives or retries run out.
- If the queue is full:
  - With **SYN cookies** enabled (default on many distros when the queue overflows): the kernel does not store the request. It encodes the state in the SYN-ACK sequence number. The connection is completed only if a valid ACK comes back. This survives a SYN flood without storing a TCB per spoofed SYN. Cost: some TCP options can be dropped on the cookie path.
  - Without cookies: the SYN is **dropped**. The client retransmits. You do not RST, because a RST tells the attacker the port is open and is also wrong for a spoofed source.

**Accept queue**

- The connection **is established**. The client can already send data. That data sits in the socket buffer.
- The application has **no fd** until `accept()`.
- If the queue is full when the final ACK arrives:
  - Default (`tcp_abort_on_overflow=0`): the kernel **drops the ACK**. The client thinks the handshake stalled and retransmits the ACK. From the client's view this is a timeout, not a clean refusal. This is a classic "intermittent connection failure" with CPU idle.
  - `tcp_abort_on_overflow=1`: the kernel sends **RST**. The client fails fast. Easier to see, harsher.
- You fix an overflowing accept queue by accepting faster (more workers, less work before `accept`, a dedicated accept loop), or by raising the backlog **and** `somaxconn`, or by shedding load in front (LB). Raising the backlog without making `accept()` faster only delays the failure.

**Client-side view**

| Where it died | What the client sees |
|---|---|
| SYN dropped | SYN retransmits, then `ETIMEDOUT` (often ~3–127 seconds depending on `tcp_syn_retries`) |
| Stuck in accept queue, ACK dropped | Handshake looks done on the client (`ESTABLISHED`), then writes stall or the server RSTs later. Intermittent. |
| Server RST | `ECONNREFUSED` if RST is to a SYN, or `ECONNRESET` if the connection existed |

### Likely follow-up: SYN flood

A SYN flood fills the SYN backlog with half-open sockets from spoofed sources, so real handshakes cannot start. Mitigations: SYN cookies, `tcp_max_syn_backlog`, a firewall that rate-limits new SYNs, and an upstream scrubber. SYN cookies are the kernel's built-in answer. They do not protect the accept queue. That queue fills only after a **completed** handshake, so a flood of completed connections is an application or capacity problem (or a completed-connection attack), not a SYN flood.

### Likely follow-up: conntrack and socket exhaustion

NAT and most firewalls store a **conntrack** entry per flow. When `nf_conntrack_count` hits `nf_conntrack_max`, the kernel logs `nf_conntrack: table full, dropping packet` and new connections fail **even though the app looks idle**.

```bash
sysctl net.netfilter.nf_conntrack_count
sysctl net.netfilter.nf_conntrack_max
dmesg -T | grep -i conntrack
```

Other ceilings that look like "cannot connect":

| Ceiling | Symptom | Check |
|---|---|---|
| Per-process fds | `EMFILE` (too many open files) | `ls /proc/PID/fd \| wc -l`, `ulimit -n`, `/proc/PID/limits` |
| System-wide fds | `ENFILE` | `cat /proc/sys/fs/file-nr` |
| Ephemeral ports | client `EADDRINUSE` | `ss` TIME_WAIT count, `ip_local_port_range` |
| PID / thread limit | cannot spawn workers | `/proc/sys/kernel/threads-max`, `ulimit -u` |
| Conntrack | drops in dmesg | counters above |

---

## Q28. P99 is about 10 seconds, connections fail sometimes, CPU is ~20%, load average is ~30, no recent deploy. How do you troubleshoot?

**Definitions**

- **P99:** 99% of requests are faster than this. A 10s P99 with a healthy P50 means a **tail**, not a uniformly slow service. Tail causes: queueing, timeouts, retries, lock convoys, GC, a slow dependency on a fraction of calls.
- **Load average:** the average number of tasks in **R** (runnable) or **D** (uninterruptible sleep) over 1, 5, and 15 minutes. It is **not** a CPU percentage. Tasks in **S** (interruptible sleep: waiting on a socket, a lock with `futex`, `poll`) do **not** count.
- **CPU 20%:** user + system is low. The machine is not compute-bound. If the tool you looked at hides **iowait**, ask for it. iowait is time the CPUs were idle because runnable work was stuck on disk.

**Assumptions:** one host or one instance of the API, Linux, the 10s figure is server latency not just client timeout, "no deploy" includes config and flag changes (confirm that), load 30 is the 1-minute load.

**The reasoning they want**

CPU is not the bottleneck. Load 30 with CPU 20% means on the order of **30 tasks are runnable or stuck in D**, and they are not burning CPU. Two real pictures:

1. **Many threads in D.** Disk, NFS, or a stuck device. `iowait` is high. The API blocks on a local disk (logs, a full disk, a volume) and the tail is I/O.
2. **A multi-core box where 30 runnable threads still don't fill the CPUs.** If the host has 64 cores, load 30 is only half the cores, and 20% CPU matches "not saturated." Then load is a clue, not the cause. The 10s tail is somewhere else: a **timeout** of about 10 seconds.

**10 seconds is a suspiciously round timeout.** I look for a client timeout, a DNS timeout, a connect timeout, a pool-acquire timeout, or TCP retransmit backing off into that range. Intermittent connection **failures** plus a 10s tail, with no deploy, is usually a **resource ceiling or a dependency**, not a code bug that shipped today.

**Order of checks**

1. **Confirm the symptom is still true and where it is.** One instance or all of them? One zone? Error code (`timeout`, `connection reset`, `refused`)? P50 vs P99. If P50 is 20ms and P99 is 10s, requests are waiting, not slow to execute.
2. **Did anything else change?** Traffic mix, a certificate expiry, a DNS TTL, an upstream deploy, a full disk, a cron. "No deploy of this service" is not "nothing changed."
3. **Split CPU vs I/O vs sockets** with the commands in Q30, on the host, for 30 seconds, while it is bad.
4. **Look at downstream latency with the same timestamps.** If the database or the next hop has the same 10s tail, this service is the victim.
5. **Only then** take a thread dump, `strace`, or a Go `pprof` / Python `py-spy`. Don't start in the profiler when the kernel counters are cheaper.

```
P99 = 10s, CPU = 20%, load = 30, no deploy
        |
        +-- iowait high, tasks in D -------- disk / NFS / full volume
        |
        +-- iowait low, load is just "30 on a big box"
        |       |
        |       +-- accept queue full ----- app not accept()ing, or worker pool stuck
        |       +-- CLOSE_WAIT growing ---- fd leak
        |       +-- conntrack full --------- packet drops
        |       +-- DNS slow --------------- 5s or 10s resolver timeouts
        |       +-- pool acquire = 10s ----- DB / HTTP pool exhausted
        |       +-- downstream P99 = 10s --- dependency, not us
        |
        +-- retransmits climbing ----------- loss, MTU, bad route
```

**My own analogue, said briefly if they ask "have you seen this":** at Masters, a canary with a 10s timeout failed calls that the old process allowed 60s for. CPU was not the issue. The dependency (the government portal) was slower than the new timeout. Rollback was a gateway config change, then we moved the slow call off the request path. I don't claim this exact load-average incident.

---

## Q29. If CPU isn't high, what else causes connection failures?

Say these as mechanisms, not product names.

| Mechanism | Why connections fail while CPU is low |
|---|---|
| **Accept queue overflow** | Handshake finished, app didn't `accept()`. Kernel drops the ACK or RSTs. Workers can be blocked on a dependency, so CPU is idle. |
| **FD exhaustion** | `accept()` or `connect()` returns `EMFILE` / `ENFILE`. Often caused by a CLOSE_WAIT leak. |
| **Conntrack full** | Packets dropped in netfilter before the app. |
| **Ephemeral port exhaustion** | The process is a **client** of something and TIME_WAIT fills the source-port range. |
| **DNS** | Getaddrinfo blocks the connect path. A dead resolver waits out a ~5s timeout, sometimes twice (A and AAAA) and lands near 10s. |
| **Downstream connect timeout** | TCP SYN never answered. Client retries. Your thread sits in connect. |
| **Pool exhaustion** | Every worker is waiting to borrow a DB connection. The wait is capped at the pool timeout (often 10s or 30s). CPU idle. New inbound connections pile up in the accept queue. |
| **Packet loss / blackhole** | Retransmit timers grow exponentially (1s, 2s, 4s, 8s). P99 lands on a retransmit boundary. CPU idle because the thread is asleep in the retransmit wait. |
| **Uninterruptible I/O** | Load high, CPU low, threads in D. Disk full, NFS hang, EBS/volume stall. |
| **Memory pressure** | Not "CPU." Direct reclaim, swap, or the OOM killer. A killed upstream looks like connection reset. |
| **TLS handshake stall** | CPU can be low if we are waiting on the peer or on a slow OCSP/CRL fetch. Less common. |
| **Firewall / security list / full conntrack** | SYNs leave and never return. App looks healthy. |
| **Half-open idle drop** | A middlebox drops state. The next write gets a RST. Intermittent, and it correlates with idle time, not with CPU. |
| **Thread pool capped** | Work queue wait ≈ the 10s timeout. Same shape as a connection pool. |

The pattern: **a thread is blocked on something that is not the CPU**, and a queue in front of those threads hits a timeout.

---

## Q30. How do you check memory, sockets, fds, pools, DNS, network, and downstreams?

Run these **while the errors are happening**. A green box an hour later proves nothing.

**Memory**

```bash
free -h
cat /proc/meminfo | egrep 'MemAvailable|Dirty|Writeback|AnonPages|Swap'
vmstat 1 10          # si/so = swap in/out; wa = iowait; r = runnable; b = D state
dmesg -T | egrep -i 'oom|killed process'
ps -eo pid,ppid,stat,wchan:24,pcpu,pmem,rss,comm --sort=-rss | head
```

- `b` in vmstat is the count of **D-state** tasks. If `b` is large and `wa` is high, this is I/O, and it explains load ≫ CPU.
- `si/so` non-zero means swap. Latency will be terrible and CPU still "low."
- OOM lines mean someone was killed. Connection resets at that timestamp are the effect.

**Sockets and the three states**

```bash
ss -s                          # totals: TCP estab, timewait, orphan, closed
ss -tan state established | wc -l
ss -tan state time-wait   | wc -l
ss -tan state close-wait  | wc -l
ss -tan state fin-wait-1  | wc -l
ss -tan state fin-wait-2  | wc -l
ss -lnt                        # LISTEN Recv-Q vs Send-Q
ss -tanp | awk '$1=="CLOSE-WAIT"{print $6}' | sort | uniq -c | sort -nr | head
```

**File descriptors**

```bash
cat /proc/sys/fs/file-nr          # allocated, unused, max
ls /proc/PID/fd | wc -l
awk '/Max open files/ {print}' /proc/PID/limits
lsof -nP -p PID | awk '{print $5}' | sort | uniq -c | sort -nr | head
# many sock = socket leak; many REG = file leak; many FIFO = pipe leak
```

**Connection pools (application)**

The kernel cannot name your pool. Look at the app's metrics: `pool_in_use`, `pool_wait_seconds`, `acquire_timeout`. If there is no metric, the symptom in the kernel is: a small number of **ESTABLISHED** sockets to the DB port, and a large accept-queue **Recv-Q** on the API port, and threads blocked in a futex or in `read` on those few DB sockets.

```bash
ss -tanp dst :5432     # or :3306, :9000 for ClickHouse
# thread dump: py-spy dump --pid PID    or    kill -QUIT for Go (dumps stacks)
```

A healthy pool has idle connections. A stuck pool has all of them ESTABLISHED and the app threads blocked in the driver, or the app threads blocked **before** they get a connection (waiters).

**DNS**

```bash
time getent hosts api.internal.example
resolvectl query api.internal.example     # systemd-resolved
dig +stats api.internal.example
cat /etc/resolv.conf                       # how many nameservers, timeout, attempts
```

`resolv.conf` defaults (`timeout:5`, `attempts:2`) produce multi-second stalls. A and AAAA lookups can serialize. If `getent` is fast now, check whether it was slow **during** the incident (resolver metrics, or `tcpdump port 53`).

**Network path**

```bash
ip route get <downstream-ip>
ping -c 20 <downstream-ip>                 # loss, not just RTT
traceroute -n <downstream-ip>
ss -ti dst :443                            # retrans, rtt, cwnd on live sockets
nstat -az | egrep 'TcpRetransSegs|TcpExtTCPTimeouts|ListenOverflows|ListenDrops|TCPSynRetrans|Syncookies'
ip -s link                                 # RX/TX drops, errors
```

- **`ListenOverflows` / `ListenDrops`** incrementing: the accept queue overflowed. This is the direct counter for Q8.
- **`TcpRetransSegs`** climbing: loss or a black hole.
- Interface `RX dropped` often means the NIC ring is full (softirq can't keep up) even when user CPU looks modest. Check `softirq` time in `mpstat -P ALL 1`.

**Downstreams**

Time a single call the way the app does it, from this host:

```bash
curl -s -o /dev/null -w 'dns:%{time_namelookup} connect:%{time_connect} tls:%{time_appconnect} ttfb:%{time_starttransfer} total:%{time_total}\n' \
  https://downstream/health
```

If `time_namelookup` is several seconds, it is DNS. If `time_connect` is, it is the handshake (SYN backlog, firewall, routing). If `ttfb` is 10s, the dependency accepted the connection and then didn't answer. That is their tail, not yours.

**Conntrack**, if the host NATs or is a kube node:

```bash
sysctl net.netfilter.nf_conntrack_count net.netfilter.nf_conntrack_max
dmesg -T | grep conntrack | tail
```

---

## Q31. What do TIME_WAIT, CLOSE_WAIT, and FIN_WAIT tell you while troubleshooting?

Use the states as a diagnosis, not as a thing to "clear."

| If you see | It means | It does **not** mean |
|---|---|---|
| **CLOSE_WAIT growing** on the API process | The peer closed. This process is not calling `close()`. Fd leak. Eventually `EMFILE`, then new connections fail. | It does not mean the kernel is slow. Restart hides it until the leak refills. |
| **TIME_WAIT in the tens of thousands** on a server that closes first | Short connections, server is the active closer. Often normal. | It is not a reason to set `tcp_tw_recycle` (removed from Linux; it broke NATed clients). |
| **TIME_WAIT on a client / worker** that opens many outbound connections | Ephemeral-port pressure. Connects start failing with `EADDRINUSE`. | Pooling fixes the cause. Flushing TIME_WAIT does not. |
| **FIN_WAIT_1 growing** | We sent FIN and did not get ACK. The peer or the path is dropping segments, or the peer is gone and not RSTing. | |
| **FIN_WAIT_2 growing** | Peer ACKed our FIN and is not sending its FIN. Peer is half-closed on purpose, or it leaked **its** close. Our `tcp_fin_timeout` will reap these if we fully closed. | |
| **LISTEN Recv-Q near Send-Q**, plus `ListenOverflows` | Accept queue is the outage. Workers are stuck. CPU can still be 20%. | Raising `somaxconn` without freeing the workers only moves the cliff. |
| **Few CLOSE_WAIT, few TIME_WAIT, overflows not increasing, retransmits increasing** | The network path or the peer is lossy. States look boring. `ss -ti` shows retrans. | |

Tie-back to the 10s incident: I would look at CLOSE_WAIT and `ListenOverflows` **before** I look at TIME_WAIT. TIME_WAIT is usually a capacity footnote. CLOSE_WAIT and a full accept queue are outages.

---

## Q32. How do you inspect these states with `ss` and `lsof`?

**`ss` reads kernel socket tables.** It is the right tool. `netstat` is the older interface (`/proc/net/tcp`) and is often not installed.

```bash
ss -tanp
# -t tcp   -a all states (not only established)   -n numeric   -p process
```

Filter by state (state names are lowercase in the filter, with a hyphen):

```bash
ss -tanp state time-wait
ss -tanp state close-wait
ss -tanp state fin-wait-1
ss -tanp state fin-wait-2
ss -tanp state last-ack
ss -tanp state syn-recv
ss -tanp state established dport = :5432
ss -lnt                             # listeners only
ss -s                               # summary counts
```

**How to read a line**

```
ESTAB  0  0  10.0.0.8:8080  10.1.2.3:51422  users:(("api",pid=2211,fd=44))
```

- Local is `10.0.0.8:8080`, peer is `10.1.2.3:51422`. This is a server connection.
- For **non-listen** sockets, Recv-Q is unread bytes and Send-Q is unsent bytes. A large Send-Q means the peer or the path is not accepting data (the receiver window is closed, or the path is lossy).
- For **LISTEN**, Recv-Q and Send-Q mean queue depth and backlog (Q8). Don't mix these up in the interview. Say which socket state you are reading.

**`lsof` maps a socket to a process and an fd.** Slower, because it walks every fd.

```bash
lsof -nP -iTCP -sTCP:CLOSE_WAIT
lsof -nP -iTCP:8080
lsof -nP -p 2211 | awk '$5=="IPv4" || $5=="IPv6"'
```

`-n` skips DNS (important: you are debugging DNS, so do not let the tool call DNS). `-P` skips port-name lookup (`:https` vs `:443`).

**When `lsof` is the better answer:** you need the **fd number** to correlate with a thread dump ("thread 12 is blocked in read on fd 44"), or you need UNIX sockets and files in the same picture. **When `ss` is the better answer:** counts, states, queues, timers (`ss -to` shows retransmit timers).

### Likely follow-up: commands beyond `ss` / `lsof`

| Question | Command |
|---|---|
| Which syscall is this stuck thread in? | `cat /proc/PID/stack`, or `ls /proc/PID/task/*/stack`, or `py-spy` / Go `SIGQUIT` |
| Is iowait the load? | `vmstat 1`, `mpstat -P ALL 1` |
| Which disk? | `iostat -xz 1` |
| Retransmits since boot? | `nstat -az \| grep Retrans` |
| Did the accept queue overflow? | `nstat -az \| grep Listen` |
| Live capture of FINs | `tcpdump -ni any -c 50 'tcp port 8080 and tcp[tcpflags] & tcp-fin != 0'` |
| Per-connection RTT | `ss -ti` |

### Likely follow-up: what you would not do

- Do not `kill -9` to "clear CLOSE_WAIT" and call it fixed. The leak comes back. Find the missing `close` / context manager / `defer conn.Close()`.
- Do not disable SYN cookies or shrink TIME_WAIT globally as a first move.
- Do not raise every sysctl in one change. One change, one counter, so you know what moved `ListenOverflows`.
