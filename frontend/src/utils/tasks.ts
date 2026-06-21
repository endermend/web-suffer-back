import type { UserTaskStatus } from '@/types/tasks.ts'

// The backend stores deadlines as the literal Vladivostok/Asia (UTC+10) wall-clock
// numbers typed into the create form, but its API tags them with a bogus "+00:00"/"Z"
// suffix instead of converting — see Task.deadline in domain/entities/task.py. Parsing
// that string with `new Date()` would "honor" the fake offset and shift the time by
// 10 hours. This pulls the literal Y-M-D-H-M numbers out and ignores whatever
// timezone suffix is attached, then builds a Date from local components — so the
// result round-trips correctly through <input type="datetime-local"> and
// toLocaleString() no matter what timezone the browser itself runs in.
function parseDeadline(iso: string): Date {
  const match = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})(?::(\d{2}))?/.exec(iso)
  if (!match) return new Date(iso)
  const [, year, month, day, hour, minute, second] = match
  return new Date(
    Number(year),
    Number(month) - 1,
    Number(day),
    Number(hour),
    Number(minute),
    second ? Number(second) : 0,
  )
}

function formatDateShort(str: string): string {
  return parseDeadline(str).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function formatDateLong(str: string): string {
  return parseDeadline(str).toLocaleString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// Converts a backend ISO deadline into the "YYYY-MM-DDTHH:mm" shape a
// <input type="datetime-local"> expects, in local time — matching how the
// create form originally produced the string before sending it to the backend.
function toDatetimeLocalInput(iso: string): string {
  const date = parseDeadline(iso)
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`
}

// CSS class names keep their old wording (chip_graded etc.) — they're purely visual
// and already used across several components' <style> blocks, no need to churn those.
function statusChip(status: UserTaskStatus): string {
  if (status === 'accepted') return 'chip_graded'
  if (status === 'pending') return 'chip_submitted'
  if (status === 'rejected') return 'chip_rejected'
  return 'chip_assigned'
}

function statusLabel(status: UserTaskStatus): string {
  if (status === 'accepted') return 'Проверено'
  if (status === 'pending') return 'Сдано'
  if (status === 'rejected') return 'Отклонено'
  return 'Доступно'
}

export { formatDateShort, formatDateLong, toDatetimeLocalInput, parseDeadline, statusChip, statusLabel }
