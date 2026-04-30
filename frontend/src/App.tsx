import { useEffect, useMemo, useState } from 'react'
import { fetchDisplays, stopDisplay, switchDisplay } from './api'
import type { ApiError, DisplayControlResponse, DisplayInfo } from './types'
import './App.css'

function App() {
  const [displays, setDisplays] = useState<DisplayInfo[]>([])
  const [activeDisplayId, setActiveDisplayId] = useState<string | null>(null)
  const [selectedDisplayId, setSelectedDisplayId] = useState<string>('')
  const [loading, setLoading] = useState<boolean>(true)
  const [actionLoading, setActionLoading] = useState<boolean>(false)
  const [error, setError] = useState<ApiError | null>(null)
  const [lastAction, setLastAction] = useState<DisplayControlResponse | null>(null)

  const controllableDisplays = useMemo(
    () => displays.filter((display) => display.supports_control),
    [displays],
  )

  const activeDisplay = useMemo(
    () => displays.find((display) => display.id === activeDisplayId) ?? null,
    [displays, activeDisplayId],
  )

  const selectedDisplay = useMemo(
    () => displays.find((display) => display.id === selectedDisplayId) ?? null,
    [displays, selectedDisplayId],
  )

  const loadDisplays = async (): Promise<void> => {
    setLoading(true)

    try {
      const response = await fetchDisplays()
      const options = response.displays.filter((display) => display.supports_control)

      setDisplays(response.displays)
      setActiveDisplayId(response.active_display_id)
      setError(null)

      if (response.active_display_id && options.some((option) => option.id === response.active_display_id)) {
        setSelectedDisplayId(response.active_display_id)
      } else if (options.length > 0) {
        setSelectedDisplayId(options[0].id)
      } else {
        setSelectedDisplayId('')
      }
    } catch (err) {
      setError(err as ApiError)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void loadDisplays()
  }, [])

  const handleRun = async (): Promise<void> => {
    if (!selectedDisplayId) {
      return
    }

    setActionLoading(true)
    try {
      const response = await switchDisplay(selectedDisplayId)
      setLastAction(response)
      setError(null)
      await loadDisplays()
    } catch (err) {
      setError(err as ApiError)
    } finally {
      setActionLoading(false)
    }
  }

  const handleStop = async (): Promise<void> => {
    if (!activeDisplayId) {
      return
    }

    setActionLoading(true)
    try {
      const response = await stopDisplay(activeDisplayId)
      setLastAction(response)
      setError(null)
      await loadDisplays()
    } catch (err) {
      setError(err as ApiError)
    } finally {
      setActionLoading(false)
    }
  }

  return (
    <main className="control-shell">
      <section className="control-panel">
        <header className="panel-header">
          <p className="eyebrow">LED Matrix</p>
          <h1>Display Control</h1>
          <p className="subtitle">Choose a display script and control what is currently running.</p>
        </header>

        {error ? (
          <div className="alert alert-error" role="alert">
            <strong>{error.code}</strong>
            <span>{error.message}</span>
          </div>
        ) : null}

        <section className="status-grid">
          <article className="status-card">
            <h2>Active Display</h2>
            {loading ? <p>Loading display state...</p> : null}
            {!loading && activeDisplay ? (
              <>
                <p className="status-name">{activeDisplay.name}</p>
                <p className="status-meta">ID: {activeDisplay.id}</p>
                <p className="status-meta">Stability: {activeDisplay.stability}</p>
              </>
            ) : null}
            {!loading && !activeDisplay ? <p className="status-name">None active</p> : null}
          </article>

          <article className="status-card">
            <h2>Last Action</h2>
            {lastAction ? (
              <>
                <p className="status-name">{lastAction.action.toUpperCase()}</p>
                <p className="status-meta">Target: {lastAction.target_display_id}</p>
                <p className="status-meta">{new Date(lastAction.timestamp).toLocaleString()}</p>
                <p>{lastAction.message}</p>
              </>
            ) : (
              <p>No action executed yet.</p>
            )}
          </article>
        </section>

        <section className="controls" aria-label="display controls">
          <label htmlFor="display-select">Display Script</label>
          <div className="control-row">
            <select
              id="display-select"
              value={selectedDisplayId}
              onChange={(event) => setSelectedDisplayId(event.target.value)}
              disabled={loading || actionLoading || controllableDisplays.length === 0}
            >
              {controllableDisplays.length === 0 ? <option value="">No controllable displays</option> : null}
              {controllableDisplays.map((display) => (
                <option key={display.id} value={display.id}>
                  {display.name} ({display.id})
                </option>
              ))}
            </select>

            <button
              type="button"
              onClick={handleRun}
              disabled={loading || actionLoading || !selectedDisplayId}
              className="btn btn-primary"
            >
              {actionLoading ? 'Working...' : 'Run Selected'}
            </button>

            <button
              type="button"
              onClick={handleStop}
              disabled={loading || actionLoading || !activeDisplayId}
              className="btn btn-neutral"
            >
              Stop Active
            </button>
          </div>

          {selectedDisplay ? <p className="selection-note">Selected module: {selectedDisplay.module_path}</p> : null}
        </section>
      </section>
    </main>
  )
}

export default App
