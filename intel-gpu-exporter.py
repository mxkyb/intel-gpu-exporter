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


def update(data):
    igpu_engines_blitter_0_busy.set(
        data.get("BCS %", 0)
    )
    igpu_engines_blitter_0_sema.set(
        data.get("BCS se", 0.0)
    )
    igpu_engines_blitter_0_wait.set(
        data.get("BCS wa", 0.0)
    )

    igpu_engines_render_3d_0_busy.set(
        data.get("RCS %", 0)
    )
    igpu_engines_render_3d_0_sema.set(
        data.get("RCS se", 0.0)
    )
    igpu_engines_render_3d_0_wait.set(
        data.get("RCS wa", 0.0)
    )

    igpu_engines_video_0_busy.set(
        data.get("VCS %", 0)
    )
    igpu_engines_video_0_sema.set(
        data.get("VCS se", 0.0)
    )
    igpu_engines_video_0_wait.set(
        data.get("VCS wa", 0.0)
    )

    igpu_engines_video_enhance_0_busy.set(
        data.get("VECS %", 0)
    )
    igpu_engines_video_enhance_0_sema.set(data.get("VECS se", 0.0))
    igpu_engines_video_enhance_0_wait.set(
        data.get("VECS wa", 0.0)
    )

    igpu_frequency_actual.set(data.get("Freq MHz act", 0))
    igpu_frequency_requested.set(data.get("Freq MHz req", 0))

    igpu_interrupts.set(data.get("IRQ /s", 0))

    igpu_power_gpu.set(data.get("Power W gpu", 0))
    igpu_power_package.set(data.get("Power W pkg", 0))

    igpu_rc6.set(data.get("RC6 %", 0))


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
        cmd = f"intel_gpu_top -J -c {int(period)} -d {device}"
    else:
        cmd = f"intel_gpu_top -J -c {int(period)}"

    process = subprocess.Popen(
        cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    logging.info("Started " + cmd)

    if os.getenv("IS_DOCKER", False):
        for line in process.stdout:
            line = line.decode("utf-8").strip()
            values = [float(val) for val in line.split(",")]
            logging.debug(values)
            data = dict(zip(header, values))
            update(data)

    else:
        while process.poll() is None:
            read = process.stdout.readline()
            output = read.decode("utf-8").strip()

            if output == ",".join(header):
                continue

            logging.debug(output)
            values = [float(val) for val in output.split(",")]
            data = dict(zip(header, values))
            update(data)

    process.kill()

    if process.returncode != 0:
        logging.error("Error: " + process.stderr.read().decode("utf-8"))

    logging.info("Finished")
