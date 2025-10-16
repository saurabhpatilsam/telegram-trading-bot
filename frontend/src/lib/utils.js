import { clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs) {
  return twMerge(clsx(inputs))
}

export function formatDate(date) {
  return new Date(date).toLocaleString()
}

export function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount)
}

export function getSignalTypeColor(type) {
  switch (type?.toLowerCase()) {
    case 'buy':
    case 'long':
      return 'text-green-600 bg-green-50 border-green-200'
    case 'sell':
    case 'short':
      return 'text-red-600 bg-red-50 border-red-200'
    default:
      return 'text-gray-600 bg-gray-50 border-gray-200'
  }
}

export function getStatusColor(status) {
  switch (status?.toLowerCase()) {
    case 'active':
    case 'running':
      return 'text-green-600 bg-green-50'
    case 'stopped':
    case 'inactive':
      return 'text-red-600 bg-red-50'
    case 'pending':
      return 'text-yellow-600 bg-yellow-50'
    default:
      return 'text-gray-600 bg-gray-50'
  }
}
