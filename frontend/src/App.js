// import { useState } from 'react'
// import axios from 'axios'
// import { Layout, Card, Steps, Upload, Input, Button, Typography, message, List, Spin } from 'antd'
// import { UploadOutlined, FileTextOutlined, DownloadOutlined, FilePdfOutlined, RocketTwoTone } from '@ant-design/icons'
// import 'antd/dist/reset.css'

// const { Header, Content, Footer } = Layout
// const { Title, Paragraph } = Typography
// const { Step } = Steps
// const { TextArea } = Input

// function App() {
//   const [resumeFile, setResumeFile] = useState(null)
//   const [jobDesc, setJobDesc] = useState('')
//   const [results, setResults] = useState(null)
//   const [loading, setLoading] = useState(false)
//   const [latexContent, setLatexContent] = useState(null)
//   const [latexFilename, setLatexFilename] = useState('tailored_resume.tex')
//   const [pdfLoading, setPdfLoading] = useState(false)

//   const handleUpload = (info) => {
//     const fileObj = info.fileList && info.fileList[0]?.originFileObj;
//     setResumeFile(fileObj || null);
//     console.log('File selected:', fileObj);
//   }

//   const handleSubmit = async () => {
//     console.log('Submit clicked', resumeFile, jobDesc);
//     if (!resumeFile) {
//       message.error('Please upload a resume.')
//       return
//     }
//     setLoading(true)
//     setResults(null)
//     try {
//       const formData = new FormData()
//       formData.append('resume_file', resumeFile)
//       formData.append('job_description', jobDesc)
//       const res = await axios.post('http://localhost:8000/tailor', formData, {
//         headers: { 'Content-Type': 'multipart/form-data' }
//       })
//       setResults(res.data)
//       if (res.data.latex_content) {
//         setLatexContent(res.data.latex_content)
//         setLatexFilename(res.data.latex_filename || 'tailored_resume.tex')
//       } else {
//         setLatexContent(null)
//       }
//     } catch (err) {
//       message.error('Something went wrong. Is your backend running?')
//     }
//     setLoading(false)
//   }

//   const handleDownloadPDF = async () => {
//     if (!latexContent) return;
//     setPdfLoading(true);
//     try {
//       const formData = new FormData();
//       formData.append('latex_code', latexContent);
//       const res = await axios.post('http://localhost:8000/latex-to-pdf', formData, {
//         responseType: 'blob',
//       });
//       const blob = new Blob([res.data], { type: 'application/pdf' });
//       const link = document.createElement('a');
//       link.href = URL.createObjectURL(blob);
//       link.download = 'tailored_resume.pdf';
//       link.click();
//     } catch (err) {
//       message.error('Failed to generate PDF.');
//     }
//     setPdfLoading(false);
//   };

//   return (
//     <Layout style={{ minHeight: '100vh', background: 'linear-gradient(120deg, #f8fafc 0%, #e0e7ef 100%)' }}>
//       <Header style={{ background: 'white', boxShadow: '0 2px 8px #f0f1f2', display: 'flex', alignItems: 'center', gap: 16 }}>
//         <RocketTwoTone twoToneColor="#4f8cff" style={{ fontSize: 48, marginRight: 16, filter: 'drop-shadow(0 2px 8px #4f8cff33)' }} />
//         <div>
//           <Title level={3} style={{ margin: 0 }}>AI Resume Tailor</Title>
//           <Paragraph style={{ margin: 0, color: '#4f8cff' }}>Tailor your resume to any job description in seconds</Paragraph>
//         </div>
//       </Header>
//       <Content style={{ display: 'flex', justifyContent: 'center', alignItems: 'flex-start', minHeight: '80vh', padding: '40px 16px 0 16px' }}>
//         <Card style={{ maxWidth: 600, width: '100%', borderRadius: 16, boxShadow: '0 8px 32px rgba(60, 72, 100, 0.12)' }}>
//           <Steps current={latexContent ? 2 : (resumeFile ? 1 : 0)} style={{ marginBottom: 32 }}>
//             <Step title="Upload Resume" icon={<UploadOutlined />} />
//             <Step title="Paste JD" icon={<FileTextOutlined />} />
//             <Step title="Get Result" icon={<DownloadOutlined />} />
//           </Steps>
//           <div>
//             <Upload.Dragger
//               name="resume_file"
//               accept=".pdf,.tex"
//               beforeUpload={() => false}
//               maxCount={1}
//               onChange={handleUpload}
//               style={{ marginBottom: 24 }}
//             >
//               <p className="ant-upload-drag-icon"><UploadOutlined /></p>
//               <p className="ant-upload-text">Click or drag PDF/LaTeX file to this area to upload</p>
//             </Upload.Dragger>
//             <TextArea
//               rows={6}
//               placeholder="Paste job description here"
//               value={jobDesc}
//               onChange={e => setJobDesc(e.target.value)}
//               style={{ marginBottom: 24, borderRadius: 8 }}
//             />
//             <Button
//               type="primary"
//               size="large"
//               block
//               loading={loading}
//               style={{ borderRadius: 8 }}
//               onClick={handleSubmit}
//               disabled={!resumeFile}
//             >
//               Tailor My Resume
//             </Button>
//           </div>
//           {loading && <div style={{ textAlign: 'center', margin: '2rem 0' }}><Spin size="large" /></div>}
//           {results && latexContent && (
//             <div style={{ marginTop: 32 }}>
//               <Title level={4}>Tailored LaTeX Resume</Title>
//               <Input.TextArea
//                 value={latexContent}
//                 rows={12}
//                 readOnly
//                 style={{ background: '#23272e', color: '#f8f8f2', fontFamily: 'monospace', borderRadius: 8, marginBottom: 16 }}
//               />
//               <div style={{ display: 'flex', gap: 12 }}>
//                 <Button
//                   icon={<DownloadOutlined />}
//                   type="default"
//                   size="large"
//                   style={{ borderRadius: 8, flex: 1 }}
//                   onClick={() => {
//                     const blob = new Blob([latexContent], { type: 'text/x-tex' })
//                     const link = document.createElement('a')
//                     link.href = URL.createObjectURL(blob)
//                     link.download = latexFilename
//                     link.click()
//                   }}
//                 >
//                   Download Tailored LaTeX
//                 </Button>
//                 <Button
//                   icon={<FilePdfOutlined />}
//                   type="primary"
//                   size="large"
//                   style={{ borderRadius: 8, flex: 1 }}
//                   loading={pdfLoading}
//                   onClick={handleDownloadPDF}
//                 >
//                   Download PDF
//                 </Button>
//               </div>
//             </div>
//           )}
//         </Card>
//       </Content>
//       <Footer style={{ textAlign: 'center', color: '#7b8794', background: 'none', fontSize: 16 }}>
//         Made with ❤️ for job seekers | By Yaswanth Reddy Dasari
//       </Footer>
//     </Layout>
//   )
// }

// export default App


import { useState } from 'react';
import axios from 'axios';
import { Layout, Card, Steps, Upload, Input, Button, Typography, message, List, Spin, Tag, Row, Col, Divider } from 'antd';
import { UploadOutlined, FileTextOutlined, DownloadOutlined, FilePdfOutlined, RocketTwoTone, CheckCircleTwoTone, WarningTwoTone } from '@ant-design/icons';
import 'antd/dist/reset.css';

const { Header, Content, Footer } = Layout;
const { Title, Paragraph } = Typography;
const { Step } = Steps;
const { TextArea } = Input;

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDesc, setJobDesc] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [latexContent, setLatexContent] = useState(null);
  const [latexFilename, setLatexFilename] = useState('tailored_resume.tex');
  const [pdfLoading, setPdfLoading] = useState(false);

  const handleUpload = (info) => {
    const fileObj = info.fileList && info.fileList[0]?.originFileObj;
    setResumeFile(fileObj || null);
    if (!fileObj) {
      setResults(null);
      setLatexContent(null);
    }
  };

  const handleSubmit = async () => {
    if (!resumeFile) {
      message.error('Please upload a resume.');
      return;
    }
    setLoading(true);
    setResults(null);
    setLatexContent(null);
    try {
      const formData = new FormData();
      formData.append('resume_file', resumeFile);
      formData.append('job_description', jobDesc);
      const res = await axios.post('http://localhost:8000/tailor', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResults(res.data);
      if (res.data.latex_content) {
        setLatexContent(res.data.latex_content);
        setLatexFilename(res.data.latex_filename || 'tailored_resume.tex');
      } else {
        setLatexContent(null);
      }
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Something went wrong. Is your backend running?';
      message.error(errorMsg);
    }
    setLoading(false);
  };

  const handleDownloadPDF = async () => {
    if (!latexContent) return;
    setPdfLoading(true);
    try {
      const formData = new FormData();
      formData.append('latex_code', latexContent);
      const res = await axios.post('http://localhost:8000/latex-to-pdf', formData, {
        responseType: 'blob',
      });
      const blob = new Blob([res.data], { type: 'application/pdf' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = 'tailored_resume.pdf';
      link.click();
      URL.revokeObjectURL(link.href);
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Failed to generate PDF.';
      const errorDetails = err.response?.data?.details;
      message.error(errorDetails ? `${errorMsg} ${errorDetails}`: errorMsg);
    }
    setPdfLoading(false);
  };

  return (
    <Layout style={{ minHeight: '100vh', background: 'linear-gradient(120deg, #f8fafc 0%, #e0e7ef 100%)' }}>
      <Header style={{ background: 'white', boxShadow: '0 2px 8px #f0f1f2', display: 'flex', alignItems: 'center', gap: 16 }}>
        <RocketTwoTone twoToneColor="#4f8cff" style={{ fontSize: 48, marginRight: 16, filter: 'drop-shadow(0 2px 8px #4f8cff33)' }} />
        <div>
          <Title level={3} style={{ margin: 0 }}>AI Resume Tailor</Title>
          <Paragraph style={{ margin: 0, color: '#4f8cff' }}>Tailor your resume to any job description in seconds</Paragraph>
        </div>
      </Header>
      <Content style={{ display: 'flex', justifyContent: 'center', alignItems: 'flex-start', minHeight: '80vh', padding: '40px 16px 0 16px' }}>
        <Card style={{ maxWidth: 800, width: '100%', borderRadius: 16, boxShadow: '0 8px 32px rgba(60, 72, 100, 0.12)' }}>
          <Steps current={results ? 2 : (resumeFile ? 1 : 0)} style={{ marginBottom: 32, padding: '0 2rem' }}>
            <Step title="Upload Resume" icon={<UploadOutlined />} />
            <Step title="Paste JD" icon={<FileTextOutlined />} />
            <Step title="Get Result" icon={<DownloadOutlined />} />
          </Steps>
          <div>
            <Upload.Dragger
              name="resume_file"
              accept=".pdf,.tex"
              beforeUpload={() => false}
              maxCount={1}
              onChange={handleUpload}
              style={{ marginBottom: 24 }}
            >
              <p className="ant-upload-drag-icon"><UploadOutlined /></p>
              <p className="ant-upload-text">Click or drag PDF/LaTeX file to this area to upload</p>
            </Upload.Dragger>
            <TextArea
              rows={6}
              placeholder="Paste job description here"
              value={jobDesc}
              onChange={e => setJobDesc(e.target.value)}
              style={{ marginBottom: 24, borderRadius: 8 }}
            />
            <Button
              type="primary"
              size="large"
              block
              loading={loading}
              style={{ borderRadius: 8 }}
              onClick={handleSubmit}
              disabled={!resumeFile}
            >
              Tailor My Resume
            </Button>
          </div>
          {loading && <div style={{ textAlign: 'center', margin: '2rem 0' }}><Spin size="large" /></div>}
          
          {results && (
            <div style={{ marginTop: 32 }}>
                <Divider>Analysis Results</Divider>
                <Row gutter={24}>
                    <Col xs={24} md={12}>
                        <List
                            header={<Title level={5}><CheckCircleTwoTone twoToneColor="#52c41a" /> Matched Skills</Title>}
                            dataSource={results.matched_skills}
                            renderItem={item => (
                                <List.Item>
                                    <Tag color="success">{item}</Tag>
                                </List.Item>
                            )}
                            bordered
                            style={{ borderRadius: 8, marginBottom: 24 }}
                        />
                    </Col>
                    <Col xs={24} md={12}>
                        <List
                            header={<Title level={5}><WarningTwoTone twoToneColor="#faad14" /> Missing Skills</Title>}
                            dataSource={results.missing_skills}
                            renderItem={item => (
                                <List.Item>
                                    <Tag color="warning">{item}</Tag>
                                </List.Item>
                            )}
                            bordered
                            style={{ borderRadius: 8, marginBottom: 24 }}
                        />
                    </Col>
                </Row>

              {latexContent && (
                <>
                  <Title level={4}>Tailored LaTeX Resume</Title>
                  <Input.TextArea
                    value={latexContent}
                    rows={12}
                    readOnly
                    style={{ background: '#23272e', color: '#f8f8f2', fontFamily: 'monospace', borderRadius: 8, marginBottom: 16 }}
                  />
                  <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
                    <Button
                      icon={<DownloadOutlined />}
                      type="default"
                      size="large"
                      style={{ borderRadius: 8, flex: 1, minWidth: '200px' }}
                      onClick={() => {
                        const blob = new Blob([latexContent], { type: 'text/x-tex' });
                        const link = document.createElement('a');
                        link.href = URL.createObjectURL(blob);
                        link.download = latexFilename;
                        link.click();
                        URL.revokeObjectURL(link.href);
                      }}
                    >
                      Download Tailored LaTeX
                    </Button>
                    <Button
                      icon={<FilePdfOutlined />}
                      type="primary"
                      size="large"
                      style={{ borderRadius: 8, flex: 1, minWidth: '200px' }}
                      loading={pdfLoading}
                      onClick={handleDownloadPDF}
                    >
                      Download as PDF
                    </Button>
                  </div>
                </>
              )}
            </div>
          )}
        </Card>
      </Content>
      <Footer style={{ textAlign: 'center', color: '#7b8794', background: 'none', fontSize: 16 }}>
        Made with ❤️ for job seekers | By Yaswanth Reddy Dasari
      </Footer>
    </Layout>
  );
}

export default App;
