import React, { useEffect, useState } from 'react'

export default function Analytics(){
  const [data, setData] = useState(null)

  useEffect(()=>{
    fetch('http://localhost:8000/api/analytics').then(r=>r.json()).then(setData)
  }, [])

  if(!data) return <div style={{padding:20}}>Loading analytics…</div>

  return (
    <div style={{padding:20}}>
      <h2>Dataset Analytics</h2>
      <p>Total items: <b>{data.n_items}</b></p>
      <p>Average price: <b>{data.avg_price?.toFixed?.(2)}</b></p>
      <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:16}}>
        <Card title="Top Brands" items={data.top_brands} />
        <Card title="Top Categories" items={data.top_categories} />
        <Card title="Colors" items={data.colors} />
      </div>
    </div>
  )
}

function Card({title, items}){
  return (
    <div style={{border:'1px solid #eee', borderRadius:8, padding:12}}>
      <h4>{title}</h4>
      <ul>
        {Object.entries(items||{}).map(([k,v]) => <li key={k}>{k}: {v}</li>)}
      </ul>
    </div>
  )
}
