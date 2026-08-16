import { STATUS_OPTIONS } from "@/features/syllabus/types";
import type { ProgressMap, SubjectStatus } from "@/features/syllabus/types";

const PROGRESS_KEY = "syllabus:progress";

const STORED_STATUSES = new Set<string>(
  // "new" is the default, so it is never written; an absent key means new.
  STATUS_OPTIONS.filter((option) => option.value !== "new").map((o) => o.value),
);

/**
 * The reader's own progress, keyed by subject slug. Hand-edited or half-written
 * storage is dropped rather than trusted — this runs before first paint, so a
 * throw here would blank the page.
 */
export function readProgress(): ProgressMap {
  if (typeof window === "undefined") return {};

  let parsed: unknown;
  try {
    const raw = localStorage.getItem(PROGRESS_KEY);
    if (!raw) return {};
    parsed = JSON.parse(raw);
  } catch {
    return {};
  }

  if (typeof parsed !== "object" || parsed === null || Array.isArray(parsed)) {
    return {};
  }

  const clean: ProgressMap = {};
  for (const [slug, status] of Object.entries(parsed)) {
    if (typeof status === "string" && STORED_STATUSES.has(status)) {
      clean[slug] = status as SubjectStatus;
    }
  }
  return clean;
}

/** Best-effort: Safari private mode and a full quota both throw on write. */
export function writeProgress(map: ProgressMap): void {
  try {
    localStorage.setItem(PROGRESS_KEY, JSON.stringify(map));
  } catch {
    // The atom still holds the change; it just won't survive a reload.
  }
}
