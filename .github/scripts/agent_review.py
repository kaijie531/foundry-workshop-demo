"""Called by the agent-review GitHub workflow.

Invokes the Foundry 'release-reviewer' agent (Responses API, authenticated with
the Foundry account key) with the PR title and CI check results, and prints the
agent's structured review to stdout.

Env:
  FOUNDRY_BASE_URL - e.g. https://<res>.services.ai.azure.com/api/projects/<proj>/openai/v1/
  FOUNDRY_KEY      - Foundry account key (stored as a GitHub secret)
  FOUNDRY_AGENT    - agent name (default: release-reviewer)
  PR_TITLE, PR_NUMBER, CHECKS - context passed by the workflow
"""

import os

from openai import OpenAI

client = OpenAI(
    base_url=os.environ["FOUNDRY_BASE_URL"],
    api_key=os.environ["FOUNDRY_KEY"],
)

prompt = (
    f"Context for review:\n"
    f"- Pull request #{os.environ.get('PR_NUMBER', '?')}: {os.environ.get('PR_TITLE', '')}\n"
    f"- CI check results: {os.environ.get('CHECKS', 'none')}\n\n"
    f"Please review and respond in your required format."
)

response = client.responses.create(
    extra_body={
        "agent_reference": {
            "type": "agent_reference",
            "name": os.environ.get("FOUNDRY_AGENT", "release-reviewer"),
        }
    },
    input=prompt,
)

print(response.output_text)
