FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY pyproject.toml .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/


# OpenTelemetry Configuration for AgentCore observability
ENV OTEL_SERVICE_NAME=vacation_planner
ENV OTEL_TRACES_EXPORTER=otlp
ENV OTEL_METRICS_EXPORTER=otlp

# AWS OpenTelemetry Distribution
ENV OTEL_PYTHON_DISTRO=aws_distro
ENV OTEL_PYTHON_CONFIGURATOR=aws_configurator

# Export Protocol
ENV OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf

# CloudWatch Integration (uncomment and configure as needed)
#ENV OTEL_EXPORTER_OTLP_LOGS_HEADERS = x-aws-log-group=agents/strands-agent-logs,x-aws-log-stream=default,x-aws-metric-namespace=agents

# Enable Agent Observability
ENV AGENT_OBSERVABILITY_ENABLED=true

# Service Identification
ENV OTEL_TRACES_SAMPLER=always_on
ENV OTEL_RESOURCE_ATTRIBUTES=service.namespace=AgentCore,service.version=1.0

EXPOSE 8080

CMD ["opentelemetry-instrument", "python", "src/vacation_planner/crew.py"]

