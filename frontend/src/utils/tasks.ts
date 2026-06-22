import type { UserTaskStatus } from '@/types/tasks.ts'

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

function toDatetimeLocalInput(iso: string): string {
  const date = parseDeadline(iso)
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`
}

function isExpired(deadline: string): boolean {
  return parseDeadline(deadline) < new Date()
}

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

export {
  formatDateShort,
  formatDateLong,
  toDatetimeLocalInput,
  parseDeadline,
  isExpired,
  statusChip,
  statusLabel,
}
