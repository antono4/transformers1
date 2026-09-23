import React from 'react';
import { motion } from 'framer-motion';

export default function ProjectCard({ project }) {
    return (
        <motion.div 
            whileHover={{ y: -10 }}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="bg-slate-800 p-6 rounded-xl shadow-xl border border-slate-700 hover:border-blue-500 transition-colors"
        >
            <h3 className="text-xl font-bold text-white mb-2">{project.title}</h3>
            <p className="text-slate-400 mb-4">{project.desc.substring(0, 100)}...</p>
            <div className="flex flex-wrap gap-2 mb-4">
                {project.tags.map(tag => (
                    <span key={tag} className="text-xs bg-blue-900 text-blue-300 px-2 py-1 rounded-full">
                        {tag}
                    </span>
                ))}
            </div>
            <button className="text-blue-400 hover:text-blue-300 text-sm font-medium transition-colors">
                View Project →
            </button>
        </motion.div>
    );
}
