# Aura - Progress

Read `../shared/aura-param-decoding.md` first. Match by title before key; then determine Forge vs Connect for param access. Decode `getParam(ext, "params")` unless `summary` is enough.


## What it does

One or more progress bars with optional overall progress.

## Decoded `params` interface

```ts
type AuraProgressStyle = "edged" | "rounded" | "circular";
type AuraProgressValueProps = { valueLabel: string; maxValue: number; show: boolean };
interface ProgressBar { progress: number; backgroundColor: AuraColor; barColor: AuraColor; labelText: string; labelColor: AuraColor; valueProps: AuraProgressValueProps; id: number; }
type AuraOverallProgressProps = Pick<ProgressBar, "backgroundColor" | "barColor" | "labelColor" | "labelText" | "id"> & { show: boolean };
interface ProgressMacroProps { height: number; shadow: boolean; style: AuraProgressStyle; bars: ProgressBar[]; overallProgressProps: AuraOverallProgressProps; }
```

## Reading guidance

Output each `labelText` with percent/progress. If `valueProps.show`, progress is relative to `maxValue` and label prefix/suffix is `valueLabel`.
