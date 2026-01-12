'use client';

import { useState } from 'react';
import { uploadPDF, ExtractionResult } from '@/lib/api';
import { VoterTable } from '@/components/VoterTable';
import { WordReplacement } from '@/components/WordReplacement';
import { UploadCloud, FileText, Loader2, AlertCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import clsx from 'clsx';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ExtractionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const [copied, setCopied] = useState(false);

  const [processedResult, setProcessedResult] = useState<ExtractionResult | null>(null);

  // Metadata state
  const [metadata, setMetadata] = useState({
    district: 'ব্রাহ্মণবাড়িয়া',
    upazila: 'সরাইল',
    union: '',
    ward_number: '',
    voter_area: '',
    voter_area_code: ''
  });

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file: File) => {
    if (file.type !== "application/pdf") {
      setError("Please upload a valid PDF file.");
      return;
    }
    setFile(file);
    setError(null);
    setResult(null);
  };

  const processFile = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      const data = await uploadPDF(file, metadata);
      setResult(data);
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || "An error occurred during processing.");
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    if (!result) return;
    const dataToUse = processedResult || result;
    const jsonString = JSON.stringify(dataToUse.data, null, 2);

    // Try modern clipboard API first
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(jsonString).then(() => {
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      }).catch(err => {
        console.error('Clipboard API failed:', err);
        fallbackCopy(jsonString);
      });
    } else {
      // Fallback for browsers that don't support clipboard API
      fallbackCopy(jsonString);
    }
  };

  const fallbackCopy = (text: string) => {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    document.body.appendChild(textArea);
    textArea.select();
    try {
      document.execCommand('copy');
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Fallback copy failed:', err);
      alert('Failed to copy to clipboard. Please copy manually.');
    }
    document.body.removeChild(textArea);
  };

  const handleApplyReplacements = (rules: Array<{ find: string, replace: string }>) => {
    if (!result) return;

    const updatedData = result.data.map(voter => {
      let updatedVoter = { ...voter };

      // Apply replacements to all text fields
      rules.forEach(rule => {
        if (rule.find && rule.replace) {
          // Use safer replacement method that handles special characters
          // Replace in all string fields
          Object.keys(updatedVoter).forEach(key => {
            const value = updatedVoter[key as keyof typeof updatedVoter];
            if (typeof value === 'string') {
              // Global replace using split/join prevents regex issues
              (updatedVoter as any)[key] = value.split(rule.find).join(rule.replace);
            }
          });
        }
      });

      return updatedVoter;
    });

    // update the original result
    setResult({
      ...result,
      data: updatedData
    });
    setProcessedResult(null); // Clear processed result as main result is updated
  };

  return (
    <main className="min-h-screen bg-zinc-50 dark:bg-zinc-950 text-zinc-900 dark:text-zinc-50 font-sans p-8">
      <div className="max-w-4xl mx-auto text-center mb-12">
        <h1 className="text-4xl font-bold tracking-tight mb-4 bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
          Bengali Voter Data Extractor
        </h1>
        <p className="text-zinc-600 dark:text-zinc-400 text-lg">
          Upload your Bengali Voter List PDF to extract structured data instantly.
        </p>
      </div>

      <div className="max-w-2xl mx-auto mb-12">
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="mb-6 p-4 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded-lg flex items-center gap-3"
            >
              <AlertCircle size={20} />
              {error}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Metadata Input Form */}
        <div className="mb-8 p-6 bg-white dark:bg-zinc-900 rounded-xl shadow border border-zinc-200 dark:border-zinc-800">
          <h2 className="text-lg font-semibold mb-4">Voter Area Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input
              type="text"
              placeholder="District (জেলা)"
              value={metadata.district}
              onChange={(e) => setMetadata({ ...metadata, district: e.target.value })}
              className="px-4 py-2 bg-zinc-50 dark:bg-zinc-800 border border-zinc-300 dark:border-zinc-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <input
              type="text"
              placeholder="Upazila (উপজেলা)"
              value={metadata.upazila}
              onChange={(e) => setMetadata({ ...metadata, upazila: e.target.value })}
              className="px-4 py-2 bg-zinc-50 dark:bg-zinc-800 border border-zinc-300 dark:border-zinc-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <select
              value={metadata.union}
              onChange={(e) => setMetadata({ ...metadata, union: e.target.value })}
              className="px-4 py-2 bg-zinc-50 dark:bg-zinc-800 border border-zinc-300 dark:border-zinc-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select Union (ইউনিয়ন)</option>
              <option value="অরুয়াইল">অরুয়াইল</option>
              <option value="চুন্টা">চুন্টা</option>
              <option value="কালিকচ্ছ">কালিকচ্ছ</option>
              <option value="নোয়াগাঁও">নোয়াগাঁও</option>
              <option value="পাক শিমুল">পাক শিমুল</option>
              <option value="সরাইল">সরাইল</option>
              <option value="শাহবাজপুর">শাহবাজপুর</option>
              <option value="শাহজাদাপুর">শাহজাদাপুর</option>
              <option value="উত্তর পানিশ্বর">উত্তর পানিশ্বর</option>
            </select>
            <select
              value={metadata.ward_number}
              onChange={(e) => setMetadata({ ...metadata, ward_number: e.target.value })}
              className="px-4 py-2 bg-zinc-50 dark:bg-zinc-800 border border-zinc-300 dark:border-zinc-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select Ward (ওয়ার্ড নং)</option>
              <option value="১">১</option>
              <option value="২">২</option>
              <option value="৩">৩</option>
              <option value="৪">৪</option>
              <option value="৫">৫</option>
              <option value="৬">৬</option>
              <option value="৭">৭</option>
              <option value="৮">৮</option>
              <option value="৯">৯</option>
            </select>
            <input
              type="text"
              placeholder="Voter Area (ভোটার এলাকা)"
              value={metadata.voter_area}
              onChange={(e) => setMetadata({ ...metadata, voter_area: e.target.value })}
              className="px-4 py-2 bg-zinc-50 dark:bg-zinc-800 border border-zinc-300 dark:border-zinc-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <input
              type="text"
              placeholder="Area Code (এলাকা কোড)"
              value={metadata.voter_area_code}
              onChange={(e) => setMetadata({ ...metadata, voter_area_code: e.target.value })}
              className="px-4 py-2 bg-zinc-50 dark:bg-zinc-800 border border-zinc-300 dark:border-zinc-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        <div
          className={clsx(
            "relative border-2 border-dashed rounded-xl p-12 transition-all duration-200 text-center cursor-pointer group",
            dragActive ? "border-blue-500 bg-blue-50 dark:bg-blue-900/10" : "border-zinc-300 dark:border-zinc-700 hover:border-zinc-400 dark:hover:border-zinc-600 bg-white dark:bg-zinc-900"
          )}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => document.getElementById('file-upload')?.click()}
        >
          <input
            id="file-upload"
            type="file"
            className="hidden"
            accept="application/pdf"
            onChange={handleChange}
          />

          <div className="flex flex-col items-center gap-4">
            <div className="p-4 rounded-full bg-zinc-100 dark:bg-zinc-800 text-zinc-400 group-hover:text-blue-500 transition-colors">
              {file ? <FileText size={40} /> : <UploadCloud size={40} />}
            </div>

            <div className="space-y-1">
              <p className="font-medium text-lg">
                {file ? file.name : "Click to upload or drag and drop"}
              </p>
              {!file && (
                <p className="text-sm text-zinc-500">PDF files only (max 10MB)</p>
              )}
            </div>

            {file && !loading && !result && (
              <button
                onClick={(e) => { e.stopPropagation(); processFile(); }}
                className="mt-4 px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors shadow-lg hover:shadow-blue-500/20"
              >
                Process PDF
              </button>
            )}

            {loading && (
              <div className="flex items-center gap-2 text-blue-600 dark:text-blue-400 mt-2">
                <Loader2 className="animate-spin" />
                <span>Processing...</span>
              </div>
            )}
          </div>
        </div>
      </div>

      <AnimatePresence>
        {result && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-8"
          >
            <div className="flex justify-center gap-8">
              <div className="p-6 bg-white dark:bg-zinc-900 rounded-xl shadow-sm border border-zinc-200 dark:border-zinc-800 text-center min-w-[200px]">
                <p className="text-3xl font-bold text-zinc-900 dark:text-zinc-100">{result.total_voters}</p>
                <p className="text-sm text-zinc-500 uppercase tracking-wider font-medium">Total Voters</p>
              </div>
            </div>

            <WordReplacement onApply={handleApplyReplacements} />

            <div className="flex justify-center gap-4 my-8">
              <button
                onClick={copyToClipboard}
                className="flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
              >
                {copied ? '✓ Copied!' : 'Copy JSON'}
              </button>
              <a
                href={`data:text/json;charset=utf-8,${encodeURIComponent(JSON.stringify((processedResult || result).data, null, 2))}`}
                download={`voters-${result.job_id}.json`}
                className="flex items-center gap-2 px-6 py-3 bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 rounded-lg hover:opacity-90 transition-opacity"
              >
                Download JSON
              </a>
            </div>

            <VoterTable result={processedResult || result} />
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  );
}
