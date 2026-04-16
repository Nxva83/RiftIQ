import { useState } from "react"

export default function Heatmaps({heatmaps, API}) {
  const [modal, setModal] = useState(null)

  const maps = Object.entries(heatmaps)
  if (!maps.length) return (
    <div>
      <div className="section-title">Heatmaps K-Means</div>
      <div className="card" style={{textAlign:"center",color:"var(--grey)",padding:40}}>
        Aucune heatmap disponible — lance <code>python heatmap.py</code>
      </div>
    </div>
  )

  return (
    <div>
      <div className="section-title">Heatmaps K-Means</div>
      <div className="heatmap-grid">
        {maps.flatMap(([mapName, types]) =>
          Object.entries(types).map(([type, url]) => (
            <div className="heatmap-card" key={`${mapName}-${type}`}
              onClick={()=>setModal(`${API}${url}`)}>
              <img src={`${API}${url}`} alt={`${mapName} ${type}`} loading="lazy"/>
              <div className="heatmap-label">
                {mapName}
                <span className={`pill pill-${type}`}>{type.toUpperCase()}</span>
              </div>
            </div>
          ))
        )}
      </div>

      {modal && (
        <div className="modal-overlay" onClick={()=>setModal(null)}>
          <img src={modal} alt="heatmap plein écran"/>
        </div>
      )}
    </div>
  )
}
