import { useQuery } from "@tanstack/react-query";

import { getSubject, listSubjects, type SubjectFilters } from "@/features/syllabus/api";

export function useSubjects(filters: SubjectFilters = {}) {
  return useQuery({
    queryKey: ["subjects", filters.category ?? "", filters.q ?? ""],
    queryFn: () => listSubjects(filters),
    staleTime: 5 * 60 * 1000,
  });
}

export function useSubject(slug: string) {
  return useQuery({
    queryKey: ["subject", slug],
    queryFn: () => getSubject(slug),
    staleTime: 5 * 60 * 1000,
  });
}
