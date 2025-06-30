import { useState } from 'react'
import axios from 'axios'

function App() {
  const [resumeFile, setResumeFile] = useState(null)
  const [jobDesc, setJobDesc] = useState('')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    if (!resumeFile) {
      setError('Please upload a resume.')
      setLoading(false)
      return
    }

    try {
      const formData = new FormData()
      formData.append('resume_file', resumeFile)
      formData.append('job_description', jobDesc)

      const res = await axios.post('http://localhost:8000/tailor', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      setResults(res.data)
    } catch (err) {
      console.error(err)
      setError('Something went wrong. Is your backend running?')
    }
    setLoading(false)
  }

  return (
    <div style={{ padding: "2rem", maxWidth: "800px", margin: "auto", fontFamily: "sans-serif" }}>
      <h1>📝 AI-Powered Resume Tailoring Assistant</h1>
      <form onSubmit={handleSubmit}>
        <h3>Upload Resume (PDF)</h3>
        <input
          type="file"
          accept=".pdf"
          style={{ width: "100%", marginBottom: "1rem" }}
          onChange={(e) => setResumeFile(e.target.files[0])}
        />
        <h3>Job Description</h3>
        <textarea
          placeholder="Paste job description here"
          rows="8"
          style={{ width: "100%", marginBottom: "1rem" }}
          onChange={(e)=>setJobDesc(e.target.value)}
        ></textarea>
        <button type="submit" style={{ padding: "0.5rem 1rem" }}>Tailor My Resume</button>
      </form>

      {loading && <p>Generating tailored suggestions...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {results && (
        <div style={{ marginTop: "2rem" }}>
          <h3>Matched Skills</h3>
          <ul>{results.matched_skills.map((skill, i) => <li key={i}>{skill}</li>)}</ul>

          <h3>Missing Skills</h3>
          <ul>{results.missing_skills.map((skill, i) => <li key={i}>{skill}</li>)}</ul>

          <h3>AI Suggestions</h3>
          <pre style={{ background: "#f4f4f4", padding: "1rem" }}>{results.suggestions}</pre>
        </div>
      )}
    </div>
  )
}

export default App
