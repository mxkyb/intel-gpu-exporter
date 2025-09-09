# intel-gpu-exporter

Get metrics from Intel GPUs

## Installation
This projects uses `uv` for managing its environment. You can install `uv`, sync the dependencies, and run the script 
with the following command:
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync --locked

# Run the script
uv run intel-gpu-exporter.py
```

### Access to `intel_gpu_top`
By default, `intel_gpu_top` requires `sudo` access, and the Docker Compose configuration below takes this into account, 
but if you want to run this locally and without `sudo`, this can be disabled by running the following:
```bash
sudo sysctl kernel.perf_event_paranoid=2
```

| :warning: WARNING                                     |
|:------------------------------------------------------|
| This has security implications, use at your own risk! |

Below is a description of the paranoia levels and how they restrict processes from accessing events:
```bash
/*
 * perf event paranoia level:
 *  -1 - not paranoid at all
 *   0 - disallow raw tracepoint access for unpriv
 *   1 - disallow cpu events for unpriv
 *   2 - disallow kernel profiling for unpriv
 *   4 - disallow all unpriv perf event use
 */
```

More information can be found here: https://www.kernel.org/doc/html/latest/admin-guide/perf-security.html

## Deployment

Runs on port 8080, gathers metrics using python and intel_gpu_top

### Docker Compose

```yaml
services:
  intel-gpu-exporter:
    image: ghcr.io/brucetony/intel-gpu-exporter:rolling
    container_name: intel-gpu-exporter
    restart: unless-stopped
    privileged: true
    pid: host
    ports:
      - 8080:8080
    volumes:
      - /dev/dri/:/dev/dri/
```

## Metrics

```bash
# HELP igpu_engines_blitter_0_busy Blitter 0 busy utilisation %
# TYPE igpu_engines_blitter_0_busy gauge
igpu_engines_blitter_0_busy 0.0
# HELP igpu_engines_blitter_0_sema Blitter 0 sema utilisation %
# TYPE igpu_engines_blitter_0_sema gauge
igpu_engines_blitter_0_sema 0.0
# HELP igpu_engines_blitter_0_wait Blitter 0 wait utilisation %
# TYPE igpu_engines_blitter_0_wait gauge
igpu_engines_blitter_0_wait 0.0
# HELP igpu_engines_render_3d_0_busy Render 3D 0 busy utilisation %
# TYPE igpu_engines_render_3d_0_busy gauge
igpu_engines_render_3d_0_busy 0.0
# HELP igpu_engines_render_3d_0_sema Render 3D 0 sema utilisation %
# TYPE igpu_engines_render_3d_0_sema gauge
igpu_engines_render_3d_0_sema 0.0
# HELP igpu_engines_render_3d_0_wait Render 3D 0 wait utilisation %
# TYPE igpu_engines_render_3d_0_wait gauge
igpu_engines_render_3d_0_wait 0.0
# HELP igpu_engines_video_0_busy Video 0 busy utilisation %
# TYPE igpu_engines_video_0_busy gauge
igpu_engines_video_0_busy 0.0
# HELP igpu_engines_video_0_sema Video 0 sema utilisation %
# TYPE igpu_engines_video_0_sema gauge
igpu_engines_video_0_sema 0.0
# HELP igpu_engines_video_0_wait Video 0 wait utilisation %
# TYPE igpu_engines_video_0_wait gauge
igpu_engines_video_0_wait 0.0
# HELP igpu_engines_video_enhance_0_busy Video Enhance 0 busy utilisation %
# TYPE igpu_engines_video_enhance_0_busy gauge
igpu_engines_video_enhance_0_busy 0.0
# HELP igpu_engines_video_enhance_0_sema Video Enhance 0 sema utilisation %
# TYPE igpu_engines_video_enhance_0_sema gauge
igpu_engines_video_enhance_0_sema 0.0
# HELP igpu_engines_video_enhance_0_wait Video Enhance 0 wait utilisation %
# TYPE igpu_engines_video_enhance_0_wait gauge
igpu_engines_video_enhance_0_wait 0.0
# HELP igpu_frequency_actual Frequency actual MHz
# TYPE igpu_frequency_actual gauge
igpu_frequency_actual 0.0
# HELP igpu_frequency_requested Frequency requested MHz
# TYPE igpu_frequency_requested gauge
igpu_frequency_requested 0.0
# HELP igpu_imc_bandwidth_reads IMC reads MiB/s
# TYPE igpu_imc_bandwidth_reads gauge
igpu_imc_bandwidth_reads 733.353818
# HELP igpu_imc_bandwidth_writes IMC writes MiB/s
# TYPE igpu_imc_bandwidth_writes gauge
igpu_imc_bandwidth_writes 166.044782
# HELP igpu_interrupts Interrupts/s
# TYPE igpu_interrupts gauge
igpu_interrupts 0.0
# HELP igpu_period Period ms
# TYPE igpu_period gauge
igpu_period 5000.241296
# HELP igpu_power_gpu GPU power W
# TYPE igpu_power_gpu gauge
igpu_power_gpu 0.0
# HELP igpu_power_package Package power W
# TYPE igpu_power_package gauge
igpu_power_package 5.480595
# HELP igpu_rc6 RC6 %
# TYPE igpu_rc6 gauge
igpu_rc6 99.999993
```
