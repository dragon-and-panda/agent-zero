import { ethers } from 'ethers'

export function shortAddress(addr) {
  if (!addr) return ''
  return `${addr.slice(0, 6)}…${addr.slice(-4)}`
}

export function formatUnits(value, decimals) {
  try {
    return ethers.formatUnits(value ?? 0, decimals)
  } catch {
    return String(value ?? '')
  }
}

export function parseUnits(value, decimals) {
  return ethers.parseUnits(String(value ?? '0'), decimals)
}

