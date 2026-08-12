import { useState, useEffect } from 'react' 
 
export default function MissionControl() { 
  const [agents, setAgents] = useState([ 
    { agent: 'AI CEO', status: 'running', task: 'Strategic planning' }, 
    { agent: 'AI CMO', status: 'running', task: 'Campaign optimization' }, 
    { agent: 'AI CFO', status: 'idle', task: 'Budget review' }, 
  ]) 
 
  return ( 
        {agents.map((agent, index) =
        ))} 
        ?? 2 opportunities detected. Review recommended. 
  ) 
} 
