'use client';

import { Citation } from '@/types';

interface QuickAnswerProps {
  answer: string;
  citations: Citation[];
  className?: string;
}

export function QuickAnswer({ answer, citations, className = '' }: QuickAnswerProps) {
  if (!answer) return null;

  // Parse citations from the answer text (assuming format like [1], [2], etc.)
  const parseAnswerWithCitations = (text: string) => {
    const citationRegex = /\[(\d+)\]/g;
    const parts = text.split(citationRegex);
    
    return parts.map((part, index) => {
      if (index % 2 === 1) {
        // This is a citation number
        const citationIndex = parseInt(part) - 1;
        const citation = citations[citationIndex];
        if (citation) {
          return (
            <a
              key={index}
              href={citation.url}
              target="_blank"
              rel="noopener noreferrer"
              className="citation"
              title={`${citation.title} - ${citation.source}`}
            >
              [{part}]
            </a>
          );
        }
        return `[${part}]`;
      }
      return part;
    });
  };

  return (
    <div className={`bg-blue-50 border border-blue-200 rounded-lg p-6 ${className}`}>
      {/* Header */}
      <div className="flex items-start space-x-3 mb-4">
        <div className="flex-shrink-0">
          <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
            <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
            </svg>
          </div>
        </div>
        <div className="flex-1">
          <h3 className="text-lg font-medium text-blue-900 mb-2">Quick Answer</h3>
          <div className="prose prose-blue max-w-none">
            <p className="text-blue-800 leading-relaxed">
              {parseAnswerWithCitations(answer)}
            </p>
          </div>
        </div>
      </div>

      {/* Sources */}
      {citations.length > 0 && (
        <div className="border-t border-blue-200 pt-4">
          <h4 className="text-sm font-medium text-blue-900 mb-3">Sources:</h4>
          <div className="space-y-2">
            {citations.map((citation, index) => (
              <div key={citation.id} className="flex items-start space-x-3">
                <span className="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-700 rounded-full flex items-center justify-center text-xs font-medium">
                  {index + 1}
                </span>
                <div className="flex-1 min-w-0">
                  <a
                    href={citation.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block text-sm text-blue-700 hover:text-blue-900 font-medium hover:underline"
                  >
                    {citation.title}
                  </a>
                  <div className="flex items-center space-x-2 mt-1">
                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-blue-100 text-blue-700">
                      {citation.source}
                    </span>
                    {citation.snippet && (
                      <span className="text-xs text-blue-600 truncate">
                        {citation.snippet}
                      </span>
                    )}
                  </div>
                </div>
                <button
                  onClick={() => navigator.clipboard.writeText(citation.url)}
                  className="flex-shrink-0 p-1 text-blue-600 hover:text-blue-800 rounded-md hover:bg-blue-100"
                  title="Copy link"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="border-t border-blue-200 pt-4 mt-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <button className="flex items-center space-x-2 text-sm text-blue-700 hover:text-blue-900">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
              </svg>
              <span>Helpful</span>
            </button>
            <button className="flex items-center space-x-2 text-sm text-blue-700 hover:text-blue-900">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 13l3 3 7-7" />
              </svg>
              <span>Mark as solved</span>
            </button>
          </div>
          <button 
            onClick={() => navigator.clipboard.writeText(answer)}
            className="flex items-center space-x-2 text-sm text-blue-700 hover:text-blue-900"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
            <span>Copy answer</span>
          </button>
        </div>
      </div>
    </div>
  );
}
