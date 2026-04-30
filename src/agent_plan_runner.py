"""
MiMo Agent Lab - minimal demo

This script is a small demo for an Agent workflow.
It does not execute system commands. It only shows how a
long-chain engineering task can be decomposed, reviewed and reported.

Use cases:
- engineering document review
- local automation workflow planning
- script draft review before execution
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class Step:
    name: str
    goal: str
    check: str
    fallback: str


class PlannerAgent:
    def plan(self, task: str) -> List[Step]:
        return [
            Step(
                name="确认任务边界",
                goal="明确资料范围、输入文件和最终交付物",
                check="任务目标清晰；不直接修改原始资料",
                fallback="回到原始任务描述重新拆分",
            ),
            Step(
                name="生成检查清单",
                goal="把复杂任务拆成可逐项确认的检查点",
                check="每个检查点都有输入、输出和判断标准",
                fallback="保留未确认项，等待人工复核",
            ),
            Step(
                name="复核风险点",
                goal="检查脚本草案、配置变更和结论中的潜在风险",
                check="高风险动作必须有人工确认条件",
                fallback="阻断未通过复核的动作",
            ),
            Step(
                name="整理阶段报告",
                goal="输出结论、证据、待确认问题和下一步建议",
                check="报告可追溯，结论不夸大",
                fallback="标记不确定项，不强行给结论",
            ),
        ]


class ReviewerAgent:
    def review(self, steps: List[Step]) -> str:
        risky_keywords = ["delete", "overwrite", "format", "remove all"]
        blocked = []

        for step in steps:
            text = f"{step.name} {step.goal} {step.check} {step.fallback}".lower()
            if any(keyword in text for keyword in risky_keywords):
                blocked.append(step.name)

        if blocked:
            return "REJECTED: high-risk step found: " + ", ".join(blocked)

        return "APPROVED: plan is reviewable, traceable and human-controlled."


class ReporterAgent:
    def render(self, task: str, steps: List[Step], review: str) -> str:
        lines = [
            "# Agent Task Report",
            "",
            f"Task: {task.strip()}",
            "",
            "## Review",
            review,
            "",
            "## Plan",
        ]

        for index, step in enumerate(steps, start=1):
            lines.extend(
                [
                    f"{index}. {step.name}",
                    f"   - Goal: {step.goal}",
                    f"   - Check: {step.check}",
                    f"   - Fallback: {step.fallback}",
                ]
            )

        return "\n".join(lines)


def main() -> None:
    task_file = Path("examples/engineering-review-task.md")
    task = task_file.read_text(encoding="utf-8") if task_file.exists() else "Plan a safe engineering review workflow."

    planner = PlannerAgent()
    reviewer = ReviewerAgent()
    reporter = ReporterAgent()

    steps = planner.plan(task)
    review = reviewer.review(steps)
    report = reporter.render(task, steps, review)

    print("[PlannerAgent] task decomposed into", len(steps), "steps")
    print("[ReviewerAgent]", review)
    print("[ReporterAgent] report generated")
    print()
    print(report)


if __name__ == "__main__":
    main()
