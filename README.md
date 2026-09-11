# Tertius Kokoro

Minimal Docker Compose and Kubernetes launchers for
[Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI), plus a dependency-free
Python client that makes the text-to-speech request easy to demonstrate.

This repository contains orchestration and examples only. Kokoro-FastAPI is an
independent Apache-2.0 project and its container images are published by its
maintainers.

## Docker: CPU

```sh
docker compose up -d
docker compose logs -f kokoro
```

The first start may take time while Docker downloads the model image. Once
ready, open:

- API documentation: <http://localhost:8880/docs>
- Web interface: <http://localhost:8880/web>
- Voice list: <http://localhost:8880/v1/audio/voices>

Generate a WAV using only Python's standard library:

```sh
python scripts/generate.py \
  --text "Hello from a local Kokoro service." \
  --voice af_heart \
  --output output/hello.wav
```

List voices:

```sh
python scripts/generate.py --list-voices
```

## Docker: NVIDIA GPU

Install the NVIDIA Container Toolkit, then run:

```sh
docker compose -f compose.yaml -f compose.gpu.yaml up -d
```

The CPU and GPU files expose the same port and API, so clients do not need to
change.

## Kubernetes

CPU:

```sh
kubectl apply -k deploy/kubernetes/base
kubectl -n tts port-forward service/kokoro-tts 8880:8880
```

NVIDIA GPU:

```sh
kubectl apply -k deploy/kubernetes/overlays/gpu
kubectl -n tts port-forward service/kokoro-tts 8880:8880
```

The GPU overlay expects a working NVIDIA device plugin and a RuntimeClass named
`nvidia`.

## PABX integration

Kokoro-FastAPI exposes an OpenAI-compatible endpoint:

```text
POST /v1/audio/speech
```

For ordinary playback, request `wav` or `mp3`. For Asterisk, request `pcm`.
Kokoro returns raw mono signed 16-bit audio at 24 kHz; save it with an `.sln24`
extension and Asterisk can play it natively.

The companion `tertius-pabx` repository generates greetings while the caller
still hears ringback, answers only when the audio is ready, then plays the
result before ringing its handsets.

## Security

The service has no authentication by default. Bind it only to trusted networks,
place an authenticated reverse proxy in front of it, or keep it internal to a
container/Kubernetes network.

## License

MIT for the files in this repository. See the upstream project for model,
container, and dependency licensing.

