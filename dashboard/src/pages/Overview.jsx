import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line, RadarChart, Radar, PolarGrid, PolarAngleAxis } from "recharts"

const C = { red:"#FF4655", cyan:"#00FFAA", gold:"#FFD700", grey:"#8A9BAA" }

const Tooltip_ = ({active,payload,label}) => active && payload?.length ? (
  <div style={{background:"#0D1926",border:"1px solid #1E2D3D",padding:"8px 12px",fontFamily:"'Share Tech Mono',monospace",fontSize:12}}>
    <div style={{color:"#8A9BAA",marginBottom:4}}>{label}</div>
    {payload.map((p,i)=><div key={i} style={{color:p.color}}>{p.name}: {typeof p.value==="number"?p.value.toFixed?p.value.toFixed(1):p.value:p.value}</div>)}
  </div>
) : null

export default function Overview({matches,wins,total,avgKda,avgHs,avgAcs,winrate}) {
  // Agents
  const agentMap = {}
  matches.forEach(m => {
    if (!agentMap[m.agent]) agentMap[m.agent] = {wins:0,total:0,kda:0}
    agentMap[m.agent].total++
    agentMap[m.agent].kda += m.kda
    if (m.won) agentMap[m.agent].wins++
  })
  const agents = Object.entries(agentMap)
    .map(([name,s])=>({name,wr:Math.round(s.wins/s.total*100),kda:(s.kda/s.total).toFixed(2),games:s.total}))
    .sort((a,b)=>b.games-a.games).slice(0,6)

  // Maps
  const mapMap = {}
  matches.forEach(m => {
    if (!mapMap[m.map_name]) mapMap[m.map_name] = {wins:0,total:0}
    mapMap[m.map_name].total++
    if (m.won) mapMap[m.map_name].wins++
  })
  const maps = Object.entries(mapMap)
    .map(([name,s])=>({name,wr:Math.round(s.wins/s.total*100),games:s.total}))
    .sort((a,b)=>b.games-a.games)

  // Trend
  const trend = matches.slice().reverse().map((m,i)=>({
    i:i+1, kda:+m.kda, hs:+m.headshot_pct, acs:m.acs
  }))

  // Radar
  const radarData = [
    {stat:"KDA",    val: Math.min(+avgKda/3*100, 100)},
    {stat:"HS%",    val: Math.min(+avgHs/40*100,  100)},
    {stat:"ACS",    val: Math.min(avgAcs/300*100,  100)},
    {stat:"Winrate",val: winrate},
    {stat:"Games",  val: Math.min(total/20*100,    100)},
  ]

  const kdaColor = avgKda >= 1.5 ? C.cyan : avgKda >= 1.0 ? C.gold : C.red
  const wrColor  = winrate >= 55  ? C.cyan : winrate >= 45  ? C.gold : C.red

  return (
    <div>
      <div className="section-title">Vue d'ensemble</div>

      {/* KPIs */}
      <div className="kpi-grid">
        {[
          {label:"Winrate",   val:`${winrate}%`,  color:wrColor},
          {label:"KDA Moy.",  val:avgKda,         color:kdaColor},
          {label:"HS% Moy.",  val:`${avgHs}%`,    color:C.gold},
          {label:"ACS Moy.",  val:avgAcs,         color:C.cyan},
          {label:"Matchs",    val:total,           color:C.grey},
        ].map((k,i)=>(
          <div className="kpi animate-up" key={i}>
            <div className="kpi-val" style={{color:k.color}}>{k.val}</div>
            <div className="kpi-label">{k.label}</div>
          </div>
        ))}
      </div>

      <div className="grid-2">
        {/* Trend KDA */}
        <div className="card">
          <div className="card-title">Évolution KDA</div>
          <ResponsiveContainer width="100%" height={180}>
            <LineChart data={trend}>
              <XAxis dataKey="i" tick={{fontSize:10}} />
              <YAxis tick={{fontSize:10}} />
              <Tooltip content={<Tooltip_/>} />
              <Line type="monotone" dataKey="kda" stroke={C.red} dot={{r:3,fill:C.red}} strokeWidth={2} name="KDA"/>
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Radar */}
        <div className="card">
          <div className="card-title">Profil joueur</div>
          <ResponsiveContainer width="100%" height={180}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="#1E2D3D"/>
              <PolarAngleAxis dataKey="stat" tick={{fill:C.grey,fontSize:11,fontFamily:"'Share Tech Mono'"}}/>
              <Radar dataKey="val" stroke={C.red} fill={C.red} fillOpacity={0.2} strokeWidth={2}/>
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid-2">
        {/* Agents */}
        <div className="card">
          <div className="card-title">Agents joués</div>
          {agents.map(a=>(
            <div className="agent-row" key={a.name}>
              <div className="agent-name">{a.name}</div>
              <div className="agent-bar-wrap">
                <div className="agent-bar" style={{width:`${a.wr}%`}}/>
              </div>
              <div className="agent-stat" style={{color: a.wr>=50?C.cyan:C.red}}>{a.wr}%</div>
              <div className="agent-stat">{a.kda}</div>
            </div>
          ))}
        </div>

        {/* Maps */}
        <div className="card">
          <div className="card-title">Winrate par map</div>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={maps} layout="vertical" barSize={14}>
              <XAxis type="number" domain={[0,100]} tick={{fontSize:10}}/>
              <YAxis type="category" dataKey="name" width={65} tick={{fontSize:11,fontFamily:"'Share Tech Mono'"}}/>
              <Tooltip content={<Tooltip_/>}/>
              <Bar dataKey="wr" name="WR%" fill={C.red} radius={[0,2,2,0]}
                label={{position:"right",fill:C.grey,fontSize:10,fontFamily:"'Share Tech Mono'",formatter:v=>`${v}%`}}/>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* ACS trend */}
      <div className="card">
        <div className="card-title">ACS & HS% par match</div>
        <ResponsiveContainer width="100%" height={160}>
          <LineChart data={trend}>
            <XAxis dataKey="i" tick={{fontSize:10}}/>
            <YAxis yAxisId="l" tick={{fontSize:10}}/>
            <YAxis yAxisId="r" orientation="right" tick={{fontSize:10}}/>
            <Tooltip content={<Tooltip_/>}/>
            <Line yAxisId="l" type="monotone" dataKey="acs" stroke={C.cyan} dot={{r:2}} strokeWidth={2} name="ACS"/>
            <Line yAxisId="r" type="monotone" dataKey="hs"  stroke={C.gold} dot={{r:2}} strokeWidth={2} name="HS%"/>
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
