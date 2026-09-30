// Calendar-level policy: how rules are generated when calendars are added, and
// plain-English descriptions of what a rule will do.

import { effectiveDetail, minDetail } from './mirror';
import { DETAIL_LABEL, type CalendarRow, type Detail, type RuleRow } from './types';

export const DEFAULT_TITLE_TEMPLATE = '{{source}}: {{title}}';
export const DEFAULT_BUSY_TITLE = 'Block';

export type RuleInsert = Omit<RuleRow, 'id'>;

export function defaultRule(source: CalendarRow, target: CalendarRow): RuleInsert {
  const detail: Detail = minDetail(source.outbound_detail, target.inbound_max_detail);
  return {
    source_calendar_id: source.id,
    target_calendar_id: target.id,
    enabled: true,
    detail,
    title_template: DEFAULT_TITLE_TEMPLATE,
    busy_title: DEFAULT_BUSY_TITLE,
    include_description: true,
    include_location: true,
    include_attendees: true,
    include_conference: true,
    visibility: 'default',
    show_as: 'busy',
    color_id: null,
    keep_reminders: false,
    buffer_before_min: 0,
    buffer_after_min: 0,
    buffer_title: 'Buffer',
    skip_all_day: true,
    skip_free: true,
    skip_declined: true,
    skip_tentative: false,
    skip_if_native_on_target: true,
    exclude_keywords: ['#nocascade'],
    lookahead_days: 60,
  };
}

export function describeRule(rule: RuleRow, source: CalendarRow, target: CalendarRow): string {
  if (!rule.enabled) return `Nothing from ${source.label} is written to ${target.label}.`;
  const detail = effectiveDetail(rule, target);
  const capped = detail !== rule.detail ? ` (capped by ${target.label}'s privacy ceiling)` : '';
  let what: string;
  if (detail === 'busy') {
    what = `a "${rule.busy_title || 'Busy'}" block with no details`;
  } else if (detail === 'title') {
    what = `an event titled "${rule.title_template.replace('{{source}}', source.label).replace('{{title}}', '<title>')}" with no other details`;
  } else {
    const parts = [
      rule.include_description && 'description',
      rule.include_location && 'location',
      rule.include_conference && 'join links',
      rule.include_attendees && 'attendees',
    ].filter(Boolean);
    what = `"${rule.title_template.replace('{{source}}', source.label).replace('{{title}}', '<title>')}"${parts.length ? ` with ${parts.join(', ')}` : ''}`;
  }
  const buffers = [
    rule.buffer_before_min && `${rule.buffer_before_min} min before`,
    rule.buffer_after_min && `${rule.buffer_after_min} min after`,
  ].filter(Boolean);
  return `${target.label} gets ${what}${capped}${buffers.length ? `, plus buffers ${buffers.join(' and ')}` : ''}.`;
}

export { DETAIL_LABEL };
