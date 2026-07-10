# Streaming Search

`EngineService.stream(...)` yields `SearchEvent` objects.

Event types:

- `started`
- `candidate`
- `completed`
- `error`

Studio can use this API to display candidates as they are discovered instead of waiting for a full result list.
