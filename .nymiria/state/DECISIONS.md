# Decision Log

*Record architectural and technical decisions here.*
## 2026-05-10 — set up the SSH config so you don't need the `-i` flag every time:
**Provider:** minimax
**Rationale:** (auto-detected)
**Source:** 🎉 **SSH is working!** Your `ade-dev2` account is connected.

Now let's set up the SSH config so you don't need the `-i` flag every time:

```bash
cat >> ~/.ssh/config << 'EOF'
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_ade_dev2
    IdentitiesOnly yes
EOF

---
