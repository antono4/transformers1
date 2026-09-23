import React from 'react';
import Head from 'next/head';
import { motion, AnimatePresence } from 'framer-motion';
import projects from '../data/projects.json';
import ProjectCard from './ProjectCard';

export default function Portfolio() {
    const [selectedProject, setSelectedProject] = useState(null);

    return (
        <div className="min-h-screen bg-slate-900 text-slate-100 font-sans selection:bg-blue-500/30">
            <Head>
                <title>DevPortfolio | Professional Software Engineer</title>
                <meta name="description" content="Portfolio of a professional developer specializing in high-performance web applications and interactive digital experiences." />
                
                {/* OpenGraph / Facebook / LinkedIn */}
                <meta property="og:type" content="website" />
                <meta property="og:url" content="https://antono4.github.io/transformers1/" />
                <meta property="og:title" content="DevPortfolio | Professional Software Engineer" />
                <meta property="og:description" content="Explore my latest projects, from high-performance web apps to interactive CLI tools. Built with Next.js and Tailwind CSS." />
                <meta property="og:image" content="https://antono4.github.io/transformers1/assets/og-image.jpg" />

                {/* Twitter */}
                <meta name="twitter:card" content="summary_large_image" />
                <meta name="twitter:title" content="DevPortfolio | Professional Software Engineer" />
                <meta name="twitter:description" content="Explore my latest projects and professional experience in modern software development." />
                <meta name="twitter:image" content="https://antono4.github.io/transformers1/assets/og-image.jpg" />
                
                <link rel="icon" href="/favicon.ico" />
            </Head>

            {/* Navigation */}
            <nav className="fixed top-0 w-full z-50 bg-slate-900/80 backdrop-blur-md border-b border-slate-800">
                <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
                    <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-blue-600 bg-clip-text text-transparent">
                        DevPortfolio
                    </span>
                    <div className="flex gap-8 text-sm font-medium text-slate-400">
                        <a href="#about" className="hover:text-white transition-colors">About</a>
                        <a href="#projects" className="hover:text-white transition-colors">Projects</a>
                        <a href="#contact" className="hover:text-white transition-colors">Contact</a>
                    </div>
                </div>
            </nav>

            {/* Hero Section */}
            <section className="pt-32 pb-20 px-6">
                <div className="max-w-4xl mx-auto text-center">
                    <motion.h1 
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="text-5xl md:text-7xl font-extrabold mb-6 tracking-tight"
                    >
                        Hi, I'm a <span className="text-blue-500">Developer</span>
                    </motion.h1>
                    <motion.p 
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.1 }}
                        className="text-lg text-slate-400 mb-10 max-w-2xl mx-auto"
                    >
                        I build beautiful, functional, and user-centric digital experiences using the latest web technologies.
                    </motion.p>
                    <motion.div 
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.2 }}
                    >
                        <a href="#projects" className="bg-blue-600 hover:bg-blue-500 text-white px-8 py-3 rounded-full font-semibold transition-all shadow-lg shadow-blue-500/20">
                            View My Work
                        </a>
                    </motion.div>
                </div>
            </section>

            {/* Projects Section */}
            <section id="projects" className="py-20 px-6 bg-slate-950/50">
                <div className="max-w-6xl mx-auto">
                    <h2 className="text-3xl font-bold text-center mb-16">Featured Projects</h2>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        {projects.map((proj) => (
                            <div key={proj.id} onClick={() => setSelectedProject(proj)}>
                                <ProjectCard project={proj} />
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Project Modal */}
            <AnimatePresence>
                {selectedProject && (
                    <motion.div 
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="fixed inset-0 z-[100] flex items-center justify-center p-6 bg-slate-900/90 backdrop-blur-sm"
                        onClick={() => setSelectedProject(null)}
                    >
                        <motion.div 
                            initial={{ scale: 0.9, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0.9, opacity: 0 }}
                            className="bg-slate-800 p-8 rounded-2xl max-w-2xl w-full border border-slate-700 relative"
                            onClick={e => e.stopPropagation()}
                        >
                            <button 
                                onClick={() => setSelectedProject(null)}
                                className="absolute top-4 right-4 text-slate-400 hover:text-white text-2xl"
                            >
                                ×
                            </button>
                            <h2 className="text-3xl font-bold mb-4">{selectedProject.title}</h2>
                            <p className="text-slate-400 mb-6 leading-relaxed">{selectedProject.desc}</p>
                            <div className="flex gap-3 mb-8">
                                {selectedProject.tags.map(tag => (
                                    <span key={tag} className="text-xs bg-slate-700 text-slate-300 px-3 py-1 rounded-full">
                                        {tag}
                                    </span>
                                ))}
                            </div>
                            <a 
                                href={selectedProject.link} 
                                className="inline-block bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-500 transition-colors"
                            >
                                Visit Project
                            </a>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
