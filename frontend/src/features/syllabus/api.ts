import { api } from "@/lib/api";
import type { Subject, SubjectDetail } from "@/features/syllabus/types";

export interface SubjectFilters {
  category?: string;
  q?: string;
}

export async function listSubjects(filters: SubjectFilters = {}): Promise<Subject[]> {
  const params = new URLSearchParams();
  if (filters.category) params.set("category", filters.category);
  if (filters.q) params.set("q", filters.q);
  const query = params.toString();
  return api<Subject[]>(`/syllabus/subjects/${query ? `?${query}` : ""}`, {
    skipAuth: true,
  });
}

export async function getSubject(slug: string): Promise<SubjectDetail> {
  return api<SubjectDetail>(`/syllabus/subjects/${slug}/`, { skipAuth: true });
}
