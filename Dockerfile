# Use a specific version for stability (SRE Best Practice)
FROM ://microsoft.com

# Set non-root user for security
RUN useradd -m appuser
USER appuser
WORKDIR /home/appuser

# Install dependencies
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy source code
COPY --chown=appuser:appuser . .

# Ensure PATH includes local bin for the appuser
ENV PATH="/home/appuser/.local/bin:${PATH}"

CMD ["python", "main.py"]
