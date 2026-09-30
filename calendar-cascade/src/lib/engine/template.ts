// {{token}} substitution for mirror titles. Unknown tokens render empty.

export const TITLE_TOKENS = ['source', 'title', 'organizer', 'location'] as const;
export type TitleVars = Partial<Record<(typeof TITLE_TOKENS)[number], string>>;

export function renderTemplate(template: string, vars: TitleVars): string {
  const out = template.replace(/\{\{\s*(\w+)\s*\}\}/g, (_, name: string) => {
    const value = (vars as Record<string, string | undefined>)[name];
    return value ?? '';
  });
  // Tidy the seams a missing token leaves behind, e.g. "Sayer: " or " ()".
  return out
    .replace(/\(\s*\)/g, '')
    .replace(/\s{2,}/g, ' ')
    .replace(/[\s:\-–—|]+$/, '')
    .trim();
}
