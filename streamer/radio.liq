#!/usr/bin/liquidsoap
log.stdout.set(true)
playlist = playlist(mode="random", reload=true, reload_mode="watch", "/music")
radio = fallback(track_sensitive=false, [playlist, blank()])
output.icecast(
    %mp3(bitrate=128),
    host="icecast",
    port=8000,
    password="hackme",
    mount="radio",
    name="RadioZZA",
    description="RadioZZA Live Stream",
    radio
)
