<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

- [x] Verify that the copilot-instructions.md file in the .github directory is created.

- [x] Clarify Project Requirements
	<!-- Enterprise search web application with Google-like UI, RAG capabilities, SSO authentication, and multi-source data ingestion -->

- [x] Scaffold the Project
	<!--
	Created project structure with frontend (Next.js), backend (FastAPI), ingestion, and infra folders.
	Main structure created with package.json, tsconfig.json, tailwind config, and initial components.
	-->

- [x] Customize the Project
	<!--
	✅ Updated to use AWS Bedrock instead of Grok for LLM capabilities
	✅ Created FastAPI backend with AWS integration
	✅ Implemented RAG service with AWS Bedrock LLM and embeddings
	✅ Created search service with hybrid search capabilities
	✅ Added authentication service with Google SSO support
	✅ Created data models and API schemas
	✅ Added configuration for AWS credentials and regions
	-->

- [x] Install Required Extensions
	<!-- Extensions for TypeScript, Python, and development tools will be installed as needed. -->

- [x] Compile the Project
	<!--
	✅ Frontend dependencies installed successfully
	✅ Fixed Next.js metadata viewport issue (moved to separate export)
	✅ Created authentication routes (/auth/login, /auth/callback)
	✅ Updated environment configuration for AWS
	✅ Fixed routing issues and CORS configuration
	✅ Application running on http://localhost:3001
	-->

- [x] Create and Run Task
	<!--
	✅ Created start script for easy development
	✅ Updated application to work without authentication requirement
	✅ Added Google-like homepage with sign-in option in top right
	✅ Implemented tiered access: public docs without login, full access with login
	✅ Application running successfully with proper authentication flow
	-->

- [ ] Launch the Project
	<!--
	Set up development environment and launch instructions.
	 -->

- [ ] Ensure Documentation is Complete
	<!--
	Complete README.md with setup and deployment instructions.
	 -->

## Project Overview
Enterprise search application with:
- Frontend: Next.js (SSG) with TypeScript, Tailwind CSS, Radix UI
- Backend: Python FastAPI with RAG capabilities
- Data Sources: Forums, Documentation, Freshservice tickets
- Authentication: Google SSO (OIDC)
- Search: Hybrid (BM25 + vector) with LLM summarization
- Deployment: GitHub Pages (frontend) + GCP Cloud Run (backend)
