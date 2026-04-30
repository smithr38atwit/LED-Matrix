export type DisplayStability = 'stable' | 'experimental' | 'broken' | 'test_only'
export type DisplayControlAction = 'start' | 'stop' | 'switch'

export interface DisplayInfo {
  id: string
  name: string
  module_path: string
  stability: DisplayStability
  supports_control: boolean
  notes?: string | null
}

export interface DisplayListResponse {
  displays: DisplayInfo[]
  active_display_id: string | null
}

export interface DisplayControlResponse {
  action: DisplayControlAction
  target_display_id: string
  previous_display_id: string | null
  active_display_id: string | null
  timestamp: string
  message: string
}

export interface ApiError {
  code: string
  message: string
}
