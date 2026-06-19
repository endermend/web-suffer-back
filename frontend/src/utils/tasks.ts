import type { Task } from '@/types/tasks.ts'

function formatDateShort(str: string): string {
  return new Date(str).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function formatDateLong(str: string): string {
  return new Date(str).toLocaleString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function statusChip(status: Task['status']): string {
  if (status === 'graded') return 'chip_graded'
  if (status === 'submitted') return 'chip_submitted'
  if (status === 'rejected') return 'chip_rejected'
  return 'chip_assigned'
}

function statusLabel(status: Task['status']): string {
  if (status === 'graded') return 'Проверено'
  if (status === 'submitted') return 'Сдано'
  if (status === 'rejected') return 'Отклонено'
  return 'Доступно'
}

export { formatDateShort, formatDateLong, statusChip, statusLabel }
