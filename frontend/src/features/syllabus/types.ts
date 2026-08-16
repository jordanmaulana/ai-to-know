export type CategorySlug =
  | "build"
  | "automate"
  | "agents"
  | "media"
  | "interface"
  | "infra";

export interface Subject {
  slug: string;
  title: string;
  one_liner: string;
  category: CategorySlug;
  category_label: string;
  became_usable_on: string | null;
}

export interface SubjectDetail extends Subject {
  what_you_can_build: string[];
  before_this: string;
  why_new: string;
  resource_url: string;
  source_url: string;
  /** Empty unless the date is an editorial anchor rather than a launch day. */
  date_note: string;
}

/** The editorial bar, served from syllabus/editorial.py so /about never restates it. */
export interface Editorial {
  bar: string;
  three_questions: { question: string; note: string }[];
  qualifies: string[];
  disqualifies: string[];
  categories: { slug: CategorySlug; label: string; note: string }[];
}

/** Where the reader is with a subject. Personal, browser-local, never sent to the API. */
export type SubjectStatus = "new" | "practicing" | "tried" | "mastered";

/** Status per subject slug. A missing key means "new" — see features/syllabus/progress.ts. */
export type ProgressMap = Record<string, SubjectStatus>;

/** Drives the picker, the stored-value validator, and the counter's ordering. */
export const STATUS_OPTIONS: {
  value: SubjectStatus;
  label: string;
  /** Terse form for the tally line, where the first-person label reads badly. */
  short: string;
}[] = [
  { value: "new", label: "New", short: "New" },
  { value: "practicing", label: "I'm practicing it", short: "Practicing" },
  { value: "tried", label: "I've tried this", short: "Tried" },
  { value: "mastered", label: "I mastered this", short: "Mastered" },
];

export const CATEGORIES: { slug: CategorySlug; label: string }[] = [
  { slug: "build", label: "Build software" },
  { slug: "automate", label: "Automate work" },
  { slug: "agents", label: "Agents" },
  { slug: "media", label: "Media" },
  { slug: "interface", label: "Interfaces" },
  { slug: "infra", label: "Infrastructure" },
];
