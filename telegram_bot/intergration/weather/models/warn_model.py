from dataclasses import dataclass

TEMPLATE = """\
{prefix} {typeName}{level}预警

{text}
"""


@dataclass
class WarnModel:
    text: str
    typeName: str
    level: str
    prefix: str = "⚠️"

    def __str__(self) -> str:
        return TEMPLATE.format(
            prefix=self.prefix,
            level=self.level,
            typeName=self.typeName,
            text=self.text
        )
