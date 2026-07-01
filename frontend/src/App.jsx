import { useState } from 'react'
import './App.css'

function App() {
  const [topic, setTopic] = useState('')
  const [tone, setTone] = useState('excited')
  const [post, setPost] = useState('')

  async function handleGenerate() {
    setPost('Generating...')

    const response = await fetch('http://localhost:8000/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ topic: topic, tone: tone }),
    })

    const data = await response.json()
    setPost(data.post)
  }

  return (
    <div style={{ maxWidth: '600px', margin: '50px auto', fontFamily: 'sans-serif' }}>
      <h1>LinkedIn Post Generator</h1>

      <label>Topic</label>
      <input
        type="text"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        placeholder="e.g. I finished my first project"
        style={{ width: '100%', padding: '8px', marginBottom: '10px' }}
      />

      <label>Tone</label>
      <select
        value={tone}
        onChange={(e) => setTone(e.target.value)}
        style={{ width: '100%', padding: '8px', marginBottom: '10px' }}
      >
        <option value="excited">Excited</option>
        <option value="professional">Professional</option>
        <option value="casual">Casual</option>
      </select>

      <button onClick={handleGenerate} style={{ padding: '10px 20px' }}>
        Generate Post
      </button>

      {post && (
        <div style={{ marginTop: '20px', padding: '15px', border: '1px solid #ccc' }}>
          {post}
        </div>
      )}
    </div>
  )
}

export default App