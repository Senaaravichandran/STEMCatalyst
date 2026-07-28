import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';

const SolutionRenderer = ({ solution }) => {
  return (
    <div className="solution-content-wrapper prose prose-blue dark:prose-invert max-w-none">
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[rehypeKatex]}
        components={{
          code({node, inline, className, children, ...props}) {
            const match = /language-(\w+)/.exec(className || '');
            return !inline ? (
              <div className="relative rounded-md bg-gray-800 my-4 shadow-md overflow-hidden">
                <div className="flex items-center justify-between px-4 py-2 bg-gray-900 text-gray-400 text-xs font-sans">
                  <span>{match ? match[1] : 'code'}</span>
                </div>
                <div className="p-4 overflow-x-auto text-sm text-gray-100 font-mono leading-relaxed">
                  <code className={className} {...props}>
                    {children}
                  </code>
                </div>
              </div>
            ) : (
              <code className="bg-blue-50 text-blue-700 px-1.5 py-0.5 rounded font-mono text-sm" {...props}>
                {children}
              </code>
            );
          },
          table({children, ...props}) {
            return (
              <div className="overflow-x-auto my-6">
                <table className="min-w-full divide-y divide-gray-300 border border-gray-200 rounded-lg shadow-sm" {...props}>
                  {children}
                </table>
              </div>
            );
          }
        }}
      >
        {solution}
      </ReactMarkdown>
    </div>
  );
};

export default SolutionRenderer;
