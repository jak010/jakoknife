from __future__ import annotations

from markdowngenerator import MarkdownGenerator

from .collecter import (DjangoEndPointCollect, GithubEndpointCollect)
from .libs.report import Report


class Application:

    def __init__(self, file_name: str, title: str, report: Report):
        self.file_name = file_name
        self.title = title

        # extra option
        self.enable_toc = True

        self.report = report

    def export(self):

        with MarkdownGenerator(filename=self.file_name, enable_write=False, enable_TOC=self.enable_toc) as doc:
            doc.addHeader(1, self.title)
            doc.writeTextLine()

            doc.addHeader(2, "Summary")
            summary = self.report.summary()
            doc.writeTextLine(' - Total API:' + str(summary['count']['total']))
            doc.writeTextLine(' - Total Admin API:' + str(summary['count']['detail']['api/admin']))
            doc.writeTextLine(' - Total User API:' + str(summary['count']['detail']['api/user']))
            doc.writeTextLine(' - Total Operation API:' + str(summary['count']['detail']['api/operation']))

            doc.writeTextLine(' - Total Test Complete:' + str(summary['count']['test']['complete']))
            doc.writeTextLine(' - Total Test Needs:' + str(summary['count']['test']['need']))

            doc.addHeader(2, "TEST Check List")

            doc.addHeader(3, 'Admin')
            for endpoint in self.report.develop_endpoint_collect.endpoints:
                if endpoint.prefix == 'api/admin/':
                    if endpoint.name is not None:
                        doc.writeTextLine(text=f" -[x] {endpoint.prefix}{endpoint.pattern}", html_escape=False)
                    else:
                        doc.writeTextLine(text=f" -[ ] {endpoint.prefix}{endpoint.pattern}", html_escape=False)

            doc.addHeader(3, 'User')
            for endpoint in self.report.develop_endpoint_collect.endpoints:
                if endpoint.prefix == 'api/user/':
                    if endpoint.name is not None:
                        doc.writeTextLine(text=f" -[x] {endpoint.prefix}{endpoint.pattern}", html_escape=False)
                    else:
                        doc.writeTextLine(text=f" -[ ] {endpoint.prefix}{endpoint.pattern}", html_escape=False)

            doc.addHeader(3, 'Operation')
            for endpoint in self.report.develop_endpoint_collect.endpoints:
                if endpoint.prefix == 'api/operation/':
                    if endpoint.name is not None:
                        doc.writeTextLine(text=f" -[x] {endpoint.prefix}{endpoint.pattern}", html_escape=False)
                    else:
                        doc.writeTextLine(text=f" -[ ] {endpoint.prefix}{endpoint.pattern}", html_escape=False)

            doc.addHeader(2, 'Document Check List')
            docs = self.report.todo_document()
            # / api / user

            doc.addHeader(3, 'Admin')
            for admin_doc in docs['/api/admin']:
                doc.writeTextLine(text=f"- [ ] {admin_doc}", html_escape=False)

            doc.addHeader(3, 'User')
            for user_doc in docs['/api/user']:
                doc.writeTextLine(text=f"- [ ] {user_doc}", html_escape=False)


if __name__ == '__main__':
    report = Report(
        github_endpoint_collect=GithubEndpointCollect(),
        django_endpoint_collect=DjangoEndPointCollect()
    )

    app = Application(file_name="output.md", title="Mac API Report", report=report)
    app.export()
