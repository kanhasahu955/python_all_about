<script setup lang="ts">
const config = useRuntimeConfig()
const apiBase = config.public.apiBase as string

const resumeFile = ref<File | null>(null)
const pasteText = ref('')

function onFileChange(e: Event) {
  const t = e.target as HTMLInputElement
  resumeFile.value = t.files?.[0] ?? null
}
const jobDescription = ref('')
const resumeId = ref<string | null>(null)
const loading = ref(false)
const error = ref('')
const result = ref<{
  fit_score: number
  strengths: string[]
  gaps: string[]
  suggestions: string[]
  summary: string
} | null>(null)

async function uploadResume() {
  error.value = ''
  result.value = null
  loading.value = true
  try {
    const fd = new FormData()
    if (resumeFile.value) fd.append('file', resumeFile.value)
    else if (pasteText.value.trim()) fd.append('text', pasteText.value.trim())
    else {
      error.value = 'Add a PDF or paste resume text.'
      return
    }
    const res = await fetch(`${apiBase}/api/resumes`, { method: 'POST', body: fd })
    if (!res.ok) throw new Error(await res.text())
    const data = await res.json()
    resumeId.value = data.resume_external_id
  } catch (e: unknown) {
    error.value = e instanceof Error ? e.message : 'Upload failed'
  } finally {
    loading.value = false
  }
}

async function analyze() {
  if (!resumeId.value || jobDescription.value.trim().length < 20) {
    error.value = 'Upload a resume first and enter a job description (20+ chars).'
    return
  }
  error.value = ''
  result.value = null
  loading.value = true
  try {
    const res = await fetch(`${apiBase}/api/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        resume_external_id: resumeId.value,
        job_description: jobDescription.value.trim(),
      }),
    })
    if (!res.ok) throw new Error(await res.text())
    const data = await res.json()
    result.value = {
      fit_score: data.fit_score,
      strengths: data.strengths,
      gaps: data.gaps,
      suggestions: data.suggestions,
      summary: data.summary,
    }
  } catch (e: unknown) {
    error.value = e instanceof Error ? e.message : 'Analysis failed'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main>
    <h1>Resume analyzer</h1>
    <p>Upload a resume, then paste a job description to get an agentic RAG analysis.</p>

    <section>
      <h2>1. Resume</h2>
      <input type="file" accept=".pdf,.txt" @change="onFileChange" />
      <p>Or paste text:</p>
      <textarea v-model="pasteText" rows="8" style="width: 100%" placeholder="Resume plain text..." />
      <p><button type="button" :disabled="loading" @click="uploadResume">Index resume</button></p>
      <p v-if="resumeId">Indexed. ID: <code>{{ resumeId }}</code></p>
    </section>

    <section>
      <h2>2. Job description</h2>
      <textarea v-model="jobDescription" rows="10" style="width: 100%" placeholder="Paste the job description..." />
      <p><button type="button" :disabled="loading || !resumeId" @click="analyze">Analyze fit</button></p>
    </section>

    <p v-if="error" style="color: crimson">{{ error }}</p>

    <section v-if="result">
      <h2>Result</h2>
      <p><strong>Fit score:</strong> {{ result.fit_score }} / 100</p>
      <p><strong>Summary:</strong> {{ result.summary }}</p>
      <h3>Strengths</h3>
      <ul>
        <li v-for="(s, i) in result.strengths" :key="'s' + i">{{ s }}</li>
      </ul>
      <h3>Gaps</h3>
      <ul>
        <li v-for="(g, i) in result.gaps" :key="'g' + i">{{ g }}</li>
      </ul>
      <h3>Suggestions</h3>
      <ul>
        <li v-for="(x, i) in result.suggestions" :key="'x' + i">{{ x }}</li>
      </ul>
    </section>
  </main>
</template>
