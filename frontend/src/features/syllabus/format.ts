const usableOnFormat = new Intl.DateTimeFormat("en-US", {
  month: "short",
  year: "numeric",
  // The API sends a bare date ("2025-08-01"), which JS parses as UTC midnight.
  // Without this, anything west of UTC renders the previous month.
  timeZone: "UTC",
});

/** "2025-08-01" -> "Aug 2025". Empty string when the date is unknown. */
export function formatUsableOn(value: string | null): string {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "";
  return usableOnFormat.format(date);
}
