import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import { Check, Info, AlertCircle, BookOpen, Target, Lightbulb } from 'lucide-react';

const SolutionRenderer = ({ solution }) => {
  // Custom renderer for different types of content blocks
  const components = {
    p: ({ children, ...props }) => {
      const text = String(children);
      
      // Check for special content patterns
      if (text.includes('This requires integrating concepts from') ||
          text.includes('Key insight:') ||
          text.includes('Important note:') ||
          text.includes('Remember that:') ||
          text.includes('Note:') ||
          text.includes('Tip:')) {
        return (
          <div className="solution-info-block">
            <div className="flex items-start space-x-3">
              <Info className="solution-checkmark mt-0.5" />
              <div className="text-gray-800" {...props}>
                {children}
              </div>
            </div>
          </div>
        );
      }
      
      // Check for step indicators
      if (text.match(/^(Step \d+|Phase \d+|Part \d+|Solution:|Answer:):/i)) {
        return (
          <div className="solution-step-block">
            <div className="flex items-start space-x-3">
              <Target className="solution-checkmark mt-0.5" />
              <div className="font-semibold text-gray-900" {...props}>
                {children}
              </div>
            </div>
          </div>
        );
      }
      
      // Check for solution insights and conclusions
      if (text.includes('Therefore') ||
          text.includes('Thus') ||
          text.includes('Hence') ||
          text.includes('In conclusion') ||
          text.includes('Final answer') ||
          text.includes('Result:')) {
        return (
          <div className="solution-note-block">
            <div className="flex items-start space-x-3">
              <Lightbulb className="solution-checkmark mt-0.5" />
              <div className="text-gray-800" {...props}>
                {children}
              </div>
            </div>
          </div>
        );
      }
      
      return (
        <p className="mb-4 text-gray-800 leading-relaxed" {...props}>
          {children}
        </p>
      );
    },
    
    blockquote: ({ children, ...props }) => (
      <div className="solution-content-block">
        <div className="flex items-start space-x-3">
          <AlertCircle className="solution-checkmark mt-1" />
          <div className="flex-1">
            {children}
          </div>
        </div>
      </div>
    ),
    
    ul: ({ children, ...props }) => (
      <div className="solution-content-block">
        <ul className="space-y-2" {...props}>
          {children}
        </ul>
      </div>
    ),
    
    ol: ({ children, ...props }) => (
      <div className="solution-content-block">
        <ol className="space-y-2" {...props}>
          {children}
        </ol>
      </div>
    ),
    
    li: ({ children, ...props }) => (
      <li className="flex items-start space-x-2 text-gray-800" {...props}>
        <Check className="solution-checkmark mt-0.5" />
        <span className="flex-1">{children}</span>
      </li>
    ),
    
    h1: ({ children, ...props }) => (
      <div className="solution-step-block mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-0 flex items-center space-x-3" {...props}>
          <BookOpen className="solution-checkmark" />
          <span>{children}</span>
        </h1>
      </div>
    ),
    
    h2: ({ children, ...props }) => (
      <div className="solution-step-block mb-4">
        <h2 className="text-xl font-semibold text-gray-900 mb-0 flex items-center space-x-3" {...props}>
          <Target className="solution-checkmark" />
          <span>{children}</span>
        </h2>
      </div>
    ),
    
    h3: ({ children, ...props }) => (
      <div className="solution-info-block mb-3">
        <h3 className="text-lg font-medium text-gray-800 mb-0 flex items-center space-x-3" {...props}>
          <Lightbulb className="solution-checkmark" />
          <span>{children}</span>
        </h3>
      </div>
    ),
    
    h4: ({ children, ...props }) => (
      <h4 className="text-base font-medium text-gray-800 mb-2 mt-4" {...props}>
        {children}
      </h4>
    ),
    
    h5: ({ children, ...props }) => (
      <h5 className="text-sm font-medium text-gray-800 mb-2 mt-3" {...props}>
        {children}
      </h5>
    ),
    
    h6: ({ children, ...props }) => (
      <h6 className="text-sm font-medium text-gray-700 mb-2 mt-3" {...props}>
        {children}
      </h6>
    ),
    
    strong: ({ children, ...props }) => (
      <strong className="font-semibold text-gray-900" {...props}>
        {children}
      </strong>
    ),
    
    em: ({ children, ...props }) => (
      <em className="italic text-gray-700" {...props}>
        {children}
      </em>
    ),
    
    code: ({ children, ...props }) => (
      <code className="bg-gray-100 text-gray-800 px-2 py-1 rounded border text-sm font-mono" {...props}>
        {children}
      </code>
    ),
    
    pre: ({ children, ...props }) => (
      <div className="solution-content-block">
        <pre className="bg-gray-50 text-gray-800 p-4 rounded-lg border overflow-x-auto" {...props}>
          {children}
        </pre>
      </div>
    ),
    
    // Handle tables if they exist
    table: ({ children, ...props }) => (
      <div className="solution-content-block">
        <div className="overflow-x-auto">
          <table className="min-w-full border-collapse border border-gray-200" {...props}>
            {children}
          </table>
        </div>
      </div>
    ),
    
    th: ({ children, ...props }) => (
      <th className="border border-gray-200 bg-gray-50 px-4 py-2 text-left font-semibold text-gray-900" {...props}>
        {children}
      </th>
    ),
    
    td: ({ children, ...props }) => (
      <td className="border border-gray-200 px-4 py-2 text-gray-800" {...props}>
        {children}
      </td>
    )
  };

  return (
    <div className="solution-content-wrapper">
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[rehypeKatex]}
        components={components}
      >
        {solution}
      </ReactMarkdown>
    </div>
  );
};

export default SolutionRenderer;
