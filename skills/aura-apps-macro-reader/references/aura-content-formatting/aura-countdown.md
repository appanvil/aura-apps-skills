# Aura - Countdown

Read `../shared/aura-param-decoding.md` first. Match by title before key; then determine Forge vs Connect for param access. Decode `getParam(ext, "params")` unless `summary` is enough.


## What it does

Countdown display to an expiry timestamp.

## Decoded `params` interface

```ts
interface CountdownProps { expires: number; lastUpdated: number; hideLabels: boolean; size: number; style: "boxes" | "circles" | "gauge"; colors: { background: AuraColor; label: AuraColor; text: AuraColor }; labels: { days: string; hours: string; minutes: string; seconds: string }; }
```

## Reading guidance

Convert `expires` epoch milliseconds to date/time; labels define displayed units.
