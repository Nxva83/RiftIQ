export default function Report({report}) {
  const lines = (report || "Aucun rapport disponible.").split("\n")
  return (
    <div>
      <div className="section-title">Rapport d'analyse</div>
      <div className="card">
        <div className="card-title">Analyse des zones — généré par NeuralIQ</div>
        <div className="report-box">
          {lines.map((line,i)=>{
            const isWarning = line.includes("⚠️") || line.includes("POINT NOIR")
            const isOk      = line.includes("✅")
            const isMap     = line.startsWith("────")
            return (
              <div key={i} style={{
                color: isWarning?"#FF4655":isOk?"#00FFAA":isMap?"#FFD700":"#8A9BAA"
              }}>{line}</div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
