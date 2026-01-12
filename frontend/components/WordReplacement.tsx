'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Minimize2, Maximize2, Plus, X, RefreshCw } from 'lucide-react';
import clsx from 'clsx';

interface ReplacementRule {
    find: string;
    replace: string;
}

interface WordReplacementProps {
    onApply: (rules: ReplacementRule[]) => void;
}

export function WordReplacement({ onApply }: WordReplacementProps) {
    const [isOpen, setIsOpen] = useState(true);
    const [rules, setRules] = useState<ReplacementRule[]>([
        { find: '', replace: '' }
    ]);

    const addRule = () => {
        setRules([...rules, { find: '', replace: '' }]);
    };

    const removeRule = (index: number) => {
        setRules(rules.filter((_, i) => i !== index));
    };

    const updateRule = (index: number, field: keyof ReplacementRule, value: string) => {
        const newRules = [...rules];
        newRules[index][field] = value;
        setRules(newRules);
    };

    const handleApply = () => {
        onApply(rules);
        setRules([{ find: '', replace: '' }]);
    };

    return (
        <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end pointer-events-none">
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: 20, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 20, scale: 0.95 }}
                        className="mb-4 w-96 bg-white dark:bg-zinc-900 rounded-xl shadow-2xl border border-zinc-200 dark:border-zinc-800 overflow-hidden pointer-events-auto"
                    >
                        <div className="p-4 border-b border-zinc-100 dark:border-zinc-800 flex justify-between items-center bg-zinc-50/50 dark:bg-zinc-900/50">
                            <div>
                                <h3 className="font-semibold text-zinc-900 dark:text-zinc-100">Word Replacement</h3>
                                <p className="text-xs text-zinc-500">Fix extraction errors globally</p>
                            </div>
                            <button
                                onClick={() => setIsOpen(false)}
                                className="p-1 hover:bg-zinc-200 dark:hover:bg-zinc-800 rounded-lg text-zinc-500 transition-colors"
                                title="Minimize"
                            >
                                <Minimize2 size={16} />
                            </button>
                        </div>

                        <div className="p-4 max-h-[60vh] overflow-y-auto">
                            <div className="space-y-3">
                                {rules.map((rule, index) => (
                                    <div key={index} className="flex gap-2">
                                        <div className="flex-1 space-y-1">
                                            <input
                                                type="text"
                                                placeholder="Find"
                                                value={rule.find}
                                                onChange={(e) => updateRule(index, 'find', e.target.value)}
                                                onKeyDown={(e) => e.key === 'Enter' && handleApply()}
                                                className="w-full px-3 py-2 bg-zinc-50 dark:bg-zinc-800 border border-zinc-300 dark:border-zinc-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                                            />
                                        </div>
                                        <div className="flex-1 space-y-1">
                                            <input
                                                type="text"
                                                placeholder="Replace"
                                                value={rule.replace}
                                                onChange={(e) => updateRule(index, 'replace', e.target.value)}
                                                onKeyDown={(e) => e.key === 'Enter' && handleApply()}
                                                className="w-full px-3 py-2 bg-zinc-50 dark:bg-zinc-800 border border-zinc-300 dark:border-zinc-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                                            />
                                        </div>
                                        {rules.length > 1 && (
                                            <button
                                                onClick={() => removeRule(index)}
                                                className="px-2 text-zinc-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                                            >
                                                <X size={16} />
                                            </button>
                                        )}
                                    </div>
                                ))}
                            </div>

                            <div className="flex gap-3 mt-4 pt-4 border-t border-zinc-100 dark:border-zinc-800">
                                <button
                                    onClick={addRule}
                                    className="flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-zinc-600 dark:text-zinc-400 bg-zinc-100 dark:bg-zinc-800 hover:bg-zinc-200 dark:hover:bg-zinc-700 rounded-lg transition-colors"
                                >
                                    <Plus size={16} />
                                    Add Rule
                                </button>
                                <button
                                    onClick={handleApply}
                                    className="flex-1 flex items-center justify-center gap-1.5 px-3 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg shadow-lg shadow-blue-500/20 transition-all hover:scale-[1.02] active:scale-[0.98]"
                                >
                                    <RefreshCw size={16} />
                                    Apply All
                                </button>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            <motion.button
                layout
                onClick={() => setIsOpen(!isOpen)}
                className={clsx(
                    "flex items-center justify-center w-12 h-12 rounded-full shadow-lg transition-colors pointer-events-auto",
                    isOpen
                        ? "bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700"
                        : "bg-blue-600 text-white hover:bg-blue-700 shadow-blue-500/30"
                )}
                title={isOpen ? "Close" : "Open Word Replacement"}
            >
                {isOpen ? <X size={24} /> : <Maximize2 size={24} />}
            </motion.button>
        </div>
    );
}
