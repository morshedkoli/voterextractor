import React, { useState } from 'react';
import { Voter, ExtractionResult } from '@/lib/api';
import { Check, ChevronRight, ChevronsRight, FileJson } from 'lucide-react';

interface VoterTableProps {
    result: ExtractionResult;
}

export const VoterTable: React.FC<VoterTableProps> = ({ result }) => {
    const voters = result.data || [];
    if (voters.length === 0) return null;

    // Group by area for display (optional, based on design preference)
    // For now, let's keep it simple and just show the table as a flat list with area columns

    return (
        <div className="w-full max-w-7xl mx-auto mt-8">
            <div className="bg-white dark:bg-zinc-900 rounded-lg shadow border border-zinc-200 dark:border-zinc-800 overflow-hidden">
                <div className="bg-zinc-50 dark:bg-zinc-800/50 px-6 py-4 border-b border-zinc-200 dark:border-zinc-800 flex justify-between items-center">
                    <h3 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">Extracted Voter Data</h3>
                    <span className="text-sm text-zinc-500 dark:text-zinc-400">{voters.length} Records</span>
                </div>
                <div className="overflow-x-auto">
                    <table className="w-full text-sm text-left whitespace-nowrap">
                        <thead className="text-xs text-zinc-500 uppercase bg-zinc-50 dark:bg-zinc-800/50 border-b border-zinc-200 dark:border-zinc-800">
                            <tr>
                                <th className="px-4 py-3 sticky left-0 bg-zinc-50 dark:bg-zinc-800/50 z-10 w-20">Serial</th>
                                <th className="px-4 py-3">Voter ID</th>
                                <th className="px-4 py-3">Name</th>
                                <th className="px-4 py-3">Father/Husband</th>
                                <th className="px-4 py-3">Mother</th>
                                <th className="px-4 py-3">Occupation</th>
                                <th className="px-4 py-3">DOB</th>
                                <th className="px-4 py-3">Address</th>
                                <th className="px-4 py-3">Area Info</th>
                            </tr>
                        </thead>
                        <tbody>
                            {voters.map((voter, idx) => (
                                <tr key={idx} className="border-b border-zinc-100 dark:border-zinc-800 hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition-colors">
                                    <td className="px-4 py-3 font-mono sticky left-0 bg-white dark:bg-zinc-900 group-hover:bg-zinc-50 dark:group-hover:bg-zinc-800/50 z-10">{voter.serial_no}</td>
                                    <td className="px-4 py-3 font-mono text-zinc-600 dark:text-zinc-400">{voter.voter_id}</td>
                                    <td className="px-4 py-3 font-medium text-zinc-900 dark:text-zinc-100">{voter.name}</td>
                                    <td className="px-4 py-3 text-zinc-600 dark:text-zinc-400">{voter.father_name}</td>
                                    <td className="px-4 py-3 text-zinc-600 dark:text-zinc-400">{voter.mother_name}</td>
                                    <td className="px-4 py-3 text-zinc-600 dark:text-zinc-400">{voter.occupation}</td>
                                    <td className="px-4 py-3 font-mono text-zinc-600 dark:text-zinc-400">{voter.date_of_birth}</td>
                                    <td className="px-4 py-3 text-zinc-600 dark:text-zinc-400 max-w-xs truncate" title={voter.address}>{voter.address}</td>
                                    <td className="px-4 py-3 text-xs text-zinc-500">
                                        <div>{voter.voter_area} ({voter.voter_area_code})</div>
                                        <div>{voter.upazila}, {voter.district}</div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};
