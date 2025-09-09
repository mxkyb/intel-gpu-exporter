import logging
import os
import subprocess

from prometheus_client import start_http_server, Gauge

header = [
    "Freq MHz req", "Freq MHz act", "IRQ /s", "RC6 %", "Power W gpu", "Power W pkg", "RCS %", "RCS se", "RCS wa",
    "BCS %", "BCS se", "BCS wa", "VCS %", "VCS se", "VCS wa", "VECS %", "VECS se", "VECS wa"
]

igpu_engines_blitter_0_busy = Gauge(
    "igpu_engines_blitter_0_busy", "Blitter 0 busy utilisation %"
)
igpu_engines_blitter_0_sema = Gauge(
    "igpu_engines_blitter_0_sema", "Blitter 0 sema utilisation %"
)
igpu_engines_blitter_0_wait = Gauge(
    "igpu_engines_blitter_0_wait", "Blitter 0 wait utilisation %"
)

igpu_engines_render_3d_0_busy = Gauge(
    "igpu_engines_render_3d_0_busy", "Render 3D 0 busy utilisation %"
)
igpu_engines_render_3d_0_sema = Gauge(
    "igpu_engines_render_3d_0_sema", "Render 3D 0 sema utilisation %"
)
igpu_engines_render_3d_0_wait = Gauge(
    "igpu_engines_render_3d_0_wait", "Render 3D 0 wait utilisation %"
)

igpu_engines_video_0_busy = Gauge(
    "igpu_engines_video_0_busy", "Video 0 busy utilisation %"
)
igpu_engines_video_0_sema = Gauge(
    "igpu_engines_video_0_sema", "Video 0 sema utilisation %"
)
igpu_engines_video_0_wait = Gauge(
    "igpu_engines_video_0_wait", "Video 0 wait utilisation %"
)

igpu_engines_video_enhance_0_busy = Gauge(
    "igpu_engines_video_enhance_0_busy", "Video Enhance 0 busy utilisation %"
)
igpu_engines_video_enhance_0_sema = Gauge(
    "igpu_engines_video_enhance_0_sema", "Video Enhance 0 sema utilisation %"
)
igpu_engines_video_enhance_0_wait = Gauge(
    "igpu_engines_video_enhance_0_wait", "Video Enhance 0 wait utilisation %"
)

igpu_frequency_actual = Gauge("igpu_frequency_actual", "Frequency actual MHz")
igpu_frequency_requested = Gauge("igpu_frequency_requested", "Frequency requested MHz")

igpu_interrupts = Gauge("igpu_interrupts", "Interrupts/s")

igpu_power_gpu = Gauge("igpu_power_gpu", "GPU power W")
igpu_power_package = Gauge("igpu_power_package", "Package power W")

igpu_rc6 = Gauge("igpu_rc6", "RC6 %")


def update(new_data: dict):
    igpu_engines_blitter_0_busy.set(new_data.get("BCS %", 0))
    igpu_engines_blitter_0_sema.set(new_data.get("BCS se", 0.0))
    igpu_engines_blitter_0_wait.set(new_data.get("BCS wa", 0.0))

    igpu_engines_render_3d_0_busy.set(new_data.get("RCS %", 0))
    igpu_engines_render_3d_0_sema.set(new_data.get("RCS se", 0.0))
    igpu_engines_render_3d_0_wait.set(new_data.get("RCS wa", 0.0))

    igpu_engines_video_0_busy.set(new_data.get("VCS %", 0))
    igpu_engines_video_0_sema.set(new_data.get("VCS se", 0.0))
    igpu_engines_video_0_wait.set(new_data.get("VCS wa", 0.0))

    igpu_engines_video_enhance_0_busy.set(new_data.get("VECS %", 0))
    igpu_engines_video_enhance_0_sema.set(new_data.get("VECS se", 0.0))
    igpu_engines_video_enhance_0_wait.set(
        new_data.get("VECS wa", 0.0)
    )

    igpu_frequency_actual.set(new_data.get("Freq MHz act", 0))
    igpu_frequency_requested.set(new_data.get("Freq MHz req", 0))

    igpu_interrupts.set(new_data.get("IRQ /s", 0))

    igpu_power_gpu.set(new_data.get("Power W gpu", 0))
    igpu_power_package.set(new_data.get("Power W pkg", 0))

    igpu_rc6.set(new_data.get("RC6 %", 0))
    

def process_line(line: str):
    """Process a line of stats from intel_gpu_top."""
    output = line.decode("utf-8").strip()

    if output == ",".join(header):
        return

    logging.debug(output)
    values = [float(val) for val in output.split(",")]
    data = dict(zip(header, values))
    update(data)
    


if __name__ == "__main__":
    if os.getenv("DEBUG", False):
        loglvl = logging.DEBUG

    else:
        loglvl = logging.INFO

    logging.basicConfig(format="%(asctime)s - %(message)s", level=loglvl)

    start_http_server(8080)

    period = os.getenv("REFRESH_PERIOD_MS", 10000)
    device = os.getenv("DEVICE")

    if device:
        cmd = f"intel_gpu_top -c -s {int(period)} -d {device}"
    else:
        cmd = f"intel_gpu_top -c -s {int(period)}"

    process = subprocess.Popen(
        cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    logging.info("Started " + cmd)

    if os.getenv("IS_DOCKER", False):
        for line in process.stdout:
            process_line(line=line)

    else:
        while process.poll() is None:
            line = process.stdout.readline()
            process_line(line=line)

    process.kill()

    if process.returncode != 0:
        logging.error("Error: " + process.stderr.read().decode("utf-8"))

    logging.info("Finished")
