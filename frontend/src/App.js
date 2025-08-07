import { useState, useEffect } from 'react';
import axios from 'axios';
import { Layout, Card, Steps, Upload, Input, Button, Typography, message, List, Spin, Tag, Row, Col, Divider, Select, Modal } from 'antd';
import { UploadOutlined, FileTextOutlined, DownloadOutlined, FilePdfOutlined, RocketTwoTone, CheckCircleTwoTone, WarningTwoTone } from '@ant-design/icons';
import 'antd/dist/reset.css';

const { Header, Content, Footer } = Layout;
const { Title, Paragraph } = Typography;
const { Step } = Steps;
const { TextArea } = Input;
const { Option } = Select;

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDesc, setJobDesc] = useState('');
  const [targetMatchPercentage, setTargetMatchPercentage] = useState(0);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [latexContent, setLatexContent] = useState(null);
  const [latexFilename, setLatexFilename] = useState('tailored_resume.tex');
  const [pdfLoading, setPdfLoading] = useState(false);
  const [textContent, setTextContent] = useState(null);
  const [disclaimerVisible, setDisclaimerVisible] = useState(true);

  useEffect(() => {
    // Show disclaimer modal on first load
    setDisclaimerVisible(true);
  }, []);

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
      formData.append('target_match_percentage', targetMatchPercentage);
      console.log('Sending request to backend with target match percentage:', targetMatchPercentage);
      const res = await axios.post('http://localhost:8000/tailor', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      console.log('Backend response:', res.data);
      console.log('Response keys:', Object.keys(res.data));
      setResults(res.data);
      if (res.data.latex_content) {
        setLatexContent(res.data.latex_content);
        setLatexFilename(res.data.latex_filename || 'tailored_resume.tex');
        setTextContent(null); // Clear any previous text content
      } else {
        setLatexContent(null);
      }
    } catch (err) {
      console.error('Frontend error:', err);
      console.error('Error response:', err.response);
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
      
      // Check if the response is actually a PDF
      const contentType = res.headers['content-type'];
      if (contentType && contentType.includes('application/pdf')) {
        const blob = new Blob([res.data], { type: 'application/pdf' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'tailored_resume.pdf';
        link.click();
        URL.revokeObjectURL(link.href);
        message.success('PDF downloaded successfully!');
      } else {
        // If not a PDF, try to parse error message
        const text = await new Response(res.data).text();
        try {
          const errorData = JSON.parse(text);
          message.error(errorData.error || 'Failed to generate PDF.');
          if (errorData.details) {
            console.error('PDF generation details:', errorData.details);
          }
        } catch {
          message.error('Failed to generate PDF. Please check if LaTeX is installed.');
        }
      }
    } catch (err) {
      console.error('PDF download error:', err);
      let errorMsg = 'Failed to generate PDF.';
      
      if (err.response) {
        if (err.response.data instanceof Blob) {
          // Try to read error from blob
          try {
            const text = await new Response(err.response.data).text();
            const errorData = JSON.parse(text);
            errorMsg = errorData.error || errorMsg;
            if (errorData.details) {
              console.error('PDF generation details:', errorData.details);
            }
          } catch {
            errorMsg = 'PDF generation failed. Please check if LaTeX is installed.';
          }
        } else {
          errorMsg = err.response.data?.error || errorMsg;
        }
      }
      
      message.error(errorMsg);
      
      // Try fallback to text version
      try {
        const textFormData = new FormData();
        textFormData.append('latex_code', latexContent);
        const textRes = await axios.post('http://localhost:8000/latex-to-text', textFormData);
        if (textRes.data.text_content) {
          setTextContent(textRes.data.text_content);
          message.info('PDF generation failed, but you can download a text version below.');
        }
      } catch (textErr) {
        console.error('Text fallback also failed:', textErr);
      }
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
      {/* Disclaimer Modal */}
      <Modal
        title={<span style={{ color: '#ad6800' }}>Disclaimer</span>}
        open={disclaimerVisible}
        onOk={() => setDisclaimerVisible(false)}
        onCancel={() => setDisclaimerVisible(false)}
        okText="I Understand"
        cancelButtonProps={{ style: { display: 'none' } }}
        centered
      >
        <div style={{ fontSize: 16, color: '#ad6800', marginBottom: 8 }}>
          <b>This tool is powered by AI.</b>
        </div>
        <div style={{ fontSize: 15, color: '#ad6800' }}>
          Your resume data will be sent to a third-party language model (LLM) for processing.<br/>
          The AI may occasionally generate inaccurate or hallucinated content.<br/>
          <b>Please review all results carefully before use.</b>
        </div>
      </Modal>
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
              style={{ marginBottom: 16, borderRadius: 8 }}
            />
            
            <div style={{ marginBottom: 24 }}>
              <div style={{ marginBottom: 8, fontWeight: 500, color: '#333' }}>
                🎯 Target Match Percentage (Optional)
              </div>
              <div style={{ fontSize: 12, color: '#666', marginBottom: 12 }}>
                Want to improve your match? Select a target percentage and we'll intelligently add relevant skills to your resume.
              </div>
              <div style={{ fontSize: 11, color: '#888', marginBottom: 12, padding: 8, backgroundColor: '#f5f5f5', borderRadius: 4 }}>
                <strong>How it works:</strong> We analyze your background and add only realistic skills that relate to your experience. 
                Skills are integrated naturally into your existing sections (experience, projects, skills) using appropriate proficiency levels.
              </div>
              <Select
                placeholder="Select target match percentage"
                value={targetMatchPercentage || undefined}
                onChange={setTargetMatchPercentage}
                style={{ width: '100%' }}
                allowClear
              >
                <Option value={70}>70% - Good Match</Option>
                <Option value={80}>80% - Strong Match</Option>
                <Option value={90}>90% - Excellent Match</Option>
                <Option value={100}>100% - Perfect Match</Option>
              </Select>
            </div>
            
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
              {/* Match Score & Recommendation Section */}
              {results.match_analysis && (
                <div style={{ marginBottom: 32 }}>
                  <Divider>Match Score & Recommendation</Divider>
                  
                  {/* Enhanced Results Section */}
                  {results.match_analysis.skills_added && results.match_analysis.skills_added.length > 0 && (
                    <div style={{ marginBottom: 24, padding: 16, backgroundColor: '#f6ffed', borderRadius: 8, border: '1px solid #b7eb8f' }}>
                      <div style={{ display: 'flex', alignItems: 'center', marginBottom: 12 }}>
                        <CheckCircleTwoTone twoToneColor="#52c41a" style={{ marginRight: 8 }} />
                        <strong style={{ color: '#52c41a' }}>Resume Enhanced!</strong>
                      </div>
                      <div style={{ marginBottom: 8 }}>
                        <strong>Target:</strong> {results.match_analysis.target_percentage}% | 
                        <strong> Original Score:</strong> {Math.round((results.match_analysis.original_overall_score || 0) * 100)}% | 
                        <strong> Enhanced Score:</strong> {Math.round((results.match_analysis.enhanced_overall_score || 0) * 100)}%
                      </div>
                      <div>
                        <strong>Skills Added:</strong> {results.match_analysis.skills_added.map(skill => 
                          <Tag color="green" key={skill} style={{ margin: '2px 4px' }}>{skill}</Tag>
                        )}
                      </div>
                    </div>
                  )}
                  
                  <Row gutter={24} align="middle">
                    <Col xs={24} md={8} style={{ textAlign: 'center', marginBottom: 16 }}>
                      <div style={{ fontSize: 48, fontWeight: 700, color: results.match_analysis.color }}>
                        {Math.round((results.match_analysis.overall_score || 0) * 100)}<span style={{ fontSize: 24 }}>%</span>
                      </div>
                      <div style={{ fontSize: 18, fontWeight: 600, color: results.match_analysis.color }}>
                        {results.match_analysis.recommendation_level}
                      </div>
                      <div style={{ color: '#888', fontSize: 14, marginTop: 4 }}>
                        {results.match_analysis.recommendation_text}
                      </div>
                    </Col>
                    <Col xs={24} md={16}>
                      <Row gutter={12}>
                        <Col span={12}>
                          <Card size="small" bordered style={{ borderRadius: 8, marginBottom: 8 }}>
                            <b>Skill Match:</b> {results.match_analysis.skill_match_percentage}%<br/>
                            <b>Experience Match:</b> {results.match_analysis.experience_match_percentage}%<br/>
                            <b>Your Experience:</b> {results.match_analysis.resume_years} yrs<br/>
                            <b>Required Experience:</b> {results.match_analysis.required_years} yrs<br/>
                          </Card>
                        </Col>
                        <Col span={12}>
                          <Card size="small" bordered style={{ borderRadius: 8, marginBottom: 8 }}>
                            <b>Missing Required Skills:</b><br/>
                            {results.match_analysis.missing_required_skills && results.match_analysis.missing_required_skills.length > 0 ? (
                              results.match_analysis.missing_required_skills.map(skill => <Tag color="red" key={skill}>{skill}</Tag>)
                            ) : <span style={{ color: '#52c41a' }}>None</span>}
                            <br/>
                            <b>Missing Preferred Skills:</b><br/>
                            {results.match_analysis.missing_preferred_skills && results.match_analysis.missing_preferred_skills.length > 0 ? (
                              results.match_analysis.missing_preferred_skills.map(skill => <Tag color="orange" key={skill}>{skill}</Tag>)
                            ) : <span style={{ color: '#52c41a' }}>None</span>}
                          </Card>
                        </Col>
                      </Row>
                    </Col>
                  </Row>
                </div>
              )}
              {/* Existing skills and resume UI follows... */}
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
               
               {textContent && (
                 <>
                   <Divider>Plain Text Version (Fallback)</Divider>
                   <div style={{ marginBottom: 16 }}>
                     <div style={{ fontSize: 12, color: '#666', marginBottom: 8 }}>
                       PDF generation failed, but here's a plain text version of your tailored resume.
                     </div>
                     <Input.TextArea
                       value={textContent}
                       rows={15}
                       readOnly
                       style={{ background: '#f5f5f5', color: '#333', fontFamily: 'monospace', borderRadius: 8, marginBottom: 16 }}
                     />
                     <Button
                       icon={<DownloadOutlined />}
                       type="default"
                       size="large"
                       style={{ borderRadius: 8 }}
                       onClick={() => {
                         const blob = new Blob([textContent], { type: 'text/plain' });
                         const link = document.createElement('a');
                         link.href = URL.createObjectURL(blob);
                         link.download = 'tailored_resume.txt';
                         link.click();
                         URL.revokeObjectURL(link.href);
                       }}
                     >
                       Download as Text File
                     </Button>
                   </div>
                 </>
               )}
            </div>
          )}
        </Card>
      </Content>
      <Footer style={{ textAlign: 'center', color: '#ad6800', background: 'none', fontSize: 14, borderTop: '1px solid #ffe58f', paddingTop: 8 }}>
        <span style={{ display: 'block', marginBottom: 4,fontSize: 12 }}>
          <b>Disclaimer:</b> This tool is powered by AI. Your data will be sent to an LLM and results may contain inaccuracies.
        </span>
        <span style={{ color: '#7b8794' }}>Made with ❤️ for job seekers | By Yaswanth Reddy Dasari</span>
      </Footer>
    </Layout>
  );
}

export default App;
