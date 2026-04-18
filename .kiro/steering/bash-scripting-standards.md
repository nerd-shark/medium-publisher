---
inclusion: fileMatch
fileMatchPattern: "*.sh,*.bash,Dockerfile,docker-compose.yml"
priority: high
---

# Bash, Docker, Kubernetes Standards

## Core Standards

**MANDATORY**: Follow `#code-quality-anti-patterns` steering document.

## Bash Requirements

### Script Header (MANDATORY)
```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
```

### Configuration (MANDATORY)
**NEVER hard-code values. Use environment variables.**

```bash
# ✅ GOOD
S3_BUCKET="${S3_BUCKET:-jabil-alm-standards-library-dev}"
AWS_REGION="${AWS_REGION:-us-east-1}"

# ❌ BAD
S3_BUCKET="jabil-alm-standards-library-dev"  # ❌
```

### Error Handling & Logging
```bash
# ✅ GOOD
log_error() { echo "[ERROR] $(date -Iseconds) $*" >&2; }
upload_to_s3() {
    [[ -f "$1" ]] || { log_error "File not found: $1"; return 1; }
    aws s3 cp "$1" "s3://${S3_BUCKET}/$2" || return 1
}
```

### Key Rules
- **Quote variables**: `"$var"` not `$var`
- **Use arrays**: `files=("a" "b")` not `files="a b"`
- **Modern syntax**: `$(cmd)` not `` `cmd` ``
- **Validate inputs**: Check args before use
- **Use readonly**: `readonly VAR="value"`

## Docker Standards

### Dockerfile (MANDATORY)
```dockerfile
# ✅ Multi-stage, non-root, health check
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
RUN useradd -m -u 1000 appuser
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --chown=appuser:appuser . /app
WORKDIR /app
USER appuser
HEALTHCHECK CMD python -c "import requests; requests.get('http://localhost:8000/health')"
CMD ["python", "main.py"]
```

### Docker Compose
```yaml
# ✅ Use env vars, health checks, resource limits
services:
  app:
    environment:
      - S3_BUCKET=${S3_BUCKET:-default}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
    deploy:
      resources:
        limits: {cpus: '1', memory: 512M}
```

## Kubernetes Standards

### Deployment (MANDATORY)
```yaml
# ✅ Security context, resources, probes, specific tag
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      serviceAccountName: app-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
      containers:
      - name: app
        image: app:v1.0.0  # ✅ Specific tag
        envFrom:
        - configMapRef: {name: app-config}
        - secretRef: {name: app-secrets}
        resources:
          requests: {cpu: 100m, memory: 128Mi}
          limits: {cpu: 500m, memory: 512Mi}
        livenessProbe:
          httpGet: {path: /health, port: 8000}
        readinessProbe:
          httpGet: {path: /ready, port: 8000}
```

### ConfigMap & Secrets
```yaml
# ✅ ConfigMap for non-sensitive
apiVersion: v1
kind: ConfigMap
metadata: {name: app-config}
data:
  S3_BUCKET: "value"

# ✅ Secret for sensitive
apiVersion: v1
kind: Secret
metadata: {name: app-secrets}
type: Opaque
stringData:
  password: "value"
```

### Container Entrypoint
```bash
#!/usr/bin/env bash
set -euo pipefail

validate_config() {
    for var in S3_BUCKET AWS_REGION DATABASE_URL; do
        [[ -n "${!var:-}" ]] || { echo "Missing: $var" >&2; exit 1; }
    done
}

wait_for_service() {
    local host=$1 port=$2 max=30 i=0
    while ! nc -z "$host" "$port"; do
        ((i++ >= max)) && { echo "Timeout: $host:$port" >&2; exit 1; }
        sleep 1
    done
}

main() {
    validate_config
    [[ -n "${DATABASE_HOST:-}" ]] && wait_for_service "$DATABASE_HOST" "${DATABASE_PORT:-5432}"
    [[ "${RUN_MIGRATIONS:-false}" == "true" ]] && python migrate.py
    exec "$@"
}

main "$@"
```

## Checklist

- [ ] No hard-coded values
- [ ] `set -euo pipefail` in bash
- [ ] Variables quoted
- [ ] Non-root user in containers
- [ ] Health checks defined
- [ ] Resource limits set
- [ ] Specific image tags (not :latest)
- [ ] ShellCheck passed

## References

**Core**: `#code-quality-anti-patterns` | **ShellCheck**: shellcheck.net

---

**Status**: Active | **Updated**: 2025-11-30
