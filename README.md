## sdns-proxy


**Highlights:**
A TCP DNS to DNS-over-TLS proxy, and a companion UDP-to-TCP DNS Proxy.
The first responds to DNS queries on port 53/tcp after getting a corresponding
response from an upstream DNS-over-TLS server (cloudflare-dns.com).
The second simply forwards the queries to the former.


**Indepth details:**

- Both the TCP-to-TLS-DNS and its UDP Proxy are written in Python 3.
- Uses [Twisted](https://twistedmatrix.com/) (a network programming framework).
- Further validates the TLS certificate hostname received from upstream server.
- UDP Proxy uses native Python 3 threading.


**Motivations:**

- Guarantees the integrity of name resolution service at the transport layer,
protecting against tampering or MITM attacks such as DNS Spoofing or Cache Poisoning.
- Helps mitigate the risks of [DNS Leaks](https://en.wikipedia.org/wiki/DNS_leak).
- Minimize effort and time needed to secure legacy applications or systems.


**Possible Improvements:**

- Connection pool, because TLS handshakes take more time than actual DNS queries.
- Caching layer, to reduce round-trips on frequently recurring queries.
- Multiple upstreams, to allow for Round-Robin and live-checks for fault-tolerance.


**Getting Down to Business:**

```bash
$ docker-compose up -d
Starting sdns-proxy_udp-proxy_1  ... done
Starting sdns-proxy_sdns-proxy_1 ... done

$ dig @127.0.0.1 -p 53 +tcp www.example.com

--or--

$ dig @127.0.0.1 -p 53 +notcp www.example.com

; <<>> DiG 9.11.4-3ubuntu5.1-Ubuntu <<>> @127.0.0.1 -p 53 +notcp www.example.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 35626
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1452
; PAD: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ("................................................................")
;; QUESTION SECTION:
;www.example.com.               IN      A

;; ANSWER SECTION:
www.example.com.        5668    IN      A       93.184.216.34

;; Query time: 103 msec
;; SERVER: 127.0.0.1#53(127.0.0.1)
;; WHEN: Mo Apr 01 01:25:23 CEST 2019
;; MSG SIZE  rcvd: 128
```
