export default function Matches({matches}) {
  return (
    <div>
      <div className="section-title">Historique des matchs</div>
      <div className="card" style={{padding:0}}>
        <div style={{display:"flex",gap:0,padding:"10px 12px",borderBottom:"1px solid var(--border)",
          fontFamily:"'Share Tech Mono',monospace",fontSize:11,color:"var(--grey)",letterSpacing:1}}>
          <span style={{width:44}}>RES</span>
          <span style={{width:104}}>AGENT</span>
          <span style={{flex:1}}>MAP</span>
          <span style={{width:95,textAlign:"center"}}>K / D / A</span>
          <span style={{width:58,textAlign:"right"}}>HS%</span>
          <span style={{width:58,textAlign:"right"}}>ACS</span>
        </div>
        {matches.map((m,i)=>(
          <div className={`match-row ${m.won?"win":"loss"}`} key={i}>
            <div className={`match-result ${m.won?"win":"loss"}`}>{m.won?"WIN":"LOSS"}</div>
            <div className="match-agent">{m.agent}</div>
            <div className="match-map">{m.map_name || "—"}</div>
            <div className="match-kda">{m.kills} / {m.deaths} / {m.assists}</div>
            <div className="match-stat" style={{color: m.headshot_pct>=25?"#FFD700":"var(--grey)"}}>
              {m.headshot_pct}%
            </div>
            <div className="match-stat" style={{color: m.acs>=200?"#00FFAA":"var(--grey)"}}>
              {m.acs}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
