> ## Documentation Index
> Fetch the complete documentation index at: https://platform.stepfun.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# StepFun Open Platform Documentation

export const HomeCards = ({items, nested = false}) => {
  const Heading = nested ? "h4" : "h3";
  return <div className="sf-qcards">
    {items.map(item => <a className="sf-qcard" href={item.href} key={item.title}>
        <div className="sf-qcard__icon">
          {item.key === "quickstart" && <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
              <path d="m13 2-3 7h7l-9 13 3-9H4z" />
            </svg>}
          {item.key === "console" && <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
              <rect x="3" y="3" width="7" height="7" rx="1" />
              <rect x="14" y="3" width="7" height="7" rx="1" />
              <rect x="3" y="14" width="7" height="7" rx="1" />
              <rect x="14" y="14" width="7" height="7" rx="1" />
            </svg>}
          {item.key === "api" && <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
              <circle cx="12" cy="12" r="3" />
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" />
            </svg>}
          {item.key === "coding" && <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
              <polyline points="16 18 22 12 16 6" />
              <polyline points="8 6 2 12 8 18" />
            </svg>}
          {item.key === "pricing" && <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
              <circle cx="12" cy="12" r="9" />
              <path d="M12 7v5l3 2" />
            </svg>}
          {item.key === "faq" && <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
              <circle cx="12" cy="12" r="9" />
              <path d="M9.1 9a3 3 0 1 1 5.8 1c0 2-3 3-3 3" />
              <path d="M12 17h.01" />
            </svg>}
        </div>
        <Heading>{item.title}</Heading>
        <p>{item.desc}</p>
      </a>)}
  </div>;
};

export const quickStartItems = [{
  "key": "quickstart",
  "title": "Quickstart",
  "desc": "Make your first API call",
  "href": "/en/quickstart/overview"
}, {
  "key": "console",
  "title": "Model Overview",
  "desc": "Compare capabilities and specifications to choose a model",
  "href": "/en/guides/models/overview"
}, {
  "key": "pricing",
  "title": "Pricing & Rate Limits",
  "desc": "Review model prices, billing and rate limits",
  "href": "/en/guides/pricing/details"
}, {
  "key": "coding",
  "title": "Developer Guides",
  "desc": "Explore reasoning, vision, audio and tool-use best practices",
  "href": "/en/guides/developer/openai"
}, {
  "key": "coding",
  "title": "Step Code",
  "desc": "Install the terminal AI agent, sign in and run your first task",
  "href": "/en/step-code/overview"
}, {
  "key": "pricing",
  "title": "Step Plan",
  "desc": "Explore subscriptions, quotas and setup instructions",
  "href": "/en/step-plan/overview"
}, {
  "key": "coding",
  "title": "Integrations",
  "desc": "Connect Step models to Claude Code, OpenClaw and other tools",
  "href": "/en/guides/developer/integrations/openclaw"
}, {
  "key": "api",
  "title": "API Reference",
  "desc": "Look up endpoints, parameters, response objects and error codes",
  "href": "/en/api-reference/chat/chat-completion-create"
}, {
  "key": "pricing",
  "title": "Model Lifecycle",
  "desc": "Check model status, retirement dates and migration guidance",
  "href": "/en/guides/model-migration"
}, {
  "key": "api",
  "title": "Policies & Legal",
  "desc": "Read platform terms and related policies",
  "href": "/en/agreement/userservice"
}];

<section className="step-home-hero" aria-labelledby="step-home-title">
  <div className="step-home-intro">
    <h1 id="step-home-title" className="step-home-title">Start building with StepFun</h1>
    <p className="step-home-description">Guides and reference for model integration, application development and ongoing maintenance.</p>
  </div>

  <div className="step-home-entry">
    <div className="step-home-actions">
      <a className="step-home-action step-home-action--primary" href="/docs/en/quickstart/overview">API quickstart<span aria-hidden="true">→</span></a>
      <a className="step-home-action" href="https://platform.stepfun.ai/interface-key">Get API key<span aria-hidden="true">↗</span></a>
      <a className="step-home-action" href="/docs/en/api-reference/chat/chat-completion-create">API reference</a>
    </div>
  </div>
</section>

<div className="step-home-lifecycle">
  <section className="step-home-stage" aria-labelledby="home-stage-1">
    <div className="step-home-stage-heading">
      <h2 id="home-stage-1">Explore models and make your first call</h2>
    </div>

    <HomeCards items={["guides/models/overview","quickstart/overview"].map(path => quickStartItems.find(item => item.href === `/en/${path}`))} />
  </section>

  <section className="step-home-stage" aria-labelledby="home-stage-2">
    <div className="step-home-stage-heading">
      <h2 id="home-stage-2">Build and test your application</h2>
    </div>

    <HomeCards items={["guides/developer/openai","api-reference/chat/chat-completion-create"].map(path => quickStartItems.find(item => item.href === `/en/${path}`))} />

    <div className="step-home-validation-links">
      <a href="/docs/en/guides/developer/exception">Handle errors<span aria-hidden="true"> →</span></a>
      <a href="/docs/en/guides/developer/troubleshooting">Troubleshoot requests<span aria-hidden="true"> →</span></a>
    </div>

    <div className="step-home-optional" role="region" aria-labelledby="home-tools">
      <h3 id="home-tools">Development tools and subscriptions</h3>

      <HomeCards nested items={["step-code/overview","step-plan/overview","guides/developer/integrations/openclaw"].map(path => quickStartItems.find(item => item.href === `/en/${path}`))} />
    </div>
  </section>

  <section className="step-home-stage" aria-labelledby="home-stage-3">
    <div className="step-home-stage-heading">
      <h2 id="home-stage-3">Platform usage and management</h2>
    </div>

    <HomeCards items={["guides/pricing/details","guides/model-migration","agreement/userservice"].map(path => quickStartItems.find(item => item.href === `/en/${path}`))} />
  </section>
</div>

<div id="model-capability-overview" />


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.