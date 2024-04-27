# from viewflow import this
# from viewflow.workflow import flow, lock, act
# from viewflow.workflow.flow import views
# # from enum import Enum
#
# from django.utils.translation import gettext_lazy as _
#
# from .models import ApplicationProcess
#
#
# class WorkPermitApplicationFlow(flow.Flow):
#     """
#     https://coderbook.com/@marcus/review-of-creating-process-flows-using-django-viewflow/
#     """
#     process_class = ApplicationProcess
#
#     process_title = _("Work Permit Application")
#
#     process_description = _(
#         "Split and synchronize work for a Verification Officer 1,Verification Officer 2, Commitee Officers and Minister "
#         "Officer"
#     )
#
#     start = (
#         flow.Start(views.CreateProcessView.as_view(fields=["text"]))  # TODO: link this to create application view
#         .Annotation(title="New message")
#         .Permission(auto_create=True)
#         .Next(this.data_capturing)  # what is the next task to do?
#     )
#
#     # Data Capture Officer if it is manual submission
#     data_capturing = (
#         flow.If(act.process.approved)
#             .Then(this.send)
#             .Else(this.end)
#     )
#
#     # Verification Officer Task, if the verification is completed if fail, then end of the process.
#     first_verification = (
#         flow.If(act.process.approved)
#             .Then(this.send)
#             .Else(this.end)
#     )
#
#     # Verification Officer Task 2, if the verification is completed if fail, then end of the process.
#     second_verification = (
#         flow.If(act.process.approved) # Decision which view to display...
#             .Then(this.send)
#             .Else(this.end)
#     )
#
#     commitee_decision = (
#         flow.If(act.process.approved)
#             .Then(this.send)
#             .Else(this.end)
#     )
#
#     decision = (
#         flow.View(views.UpdateProcessView.as_view(fields=["approved"]))
#         .Permission(auto_create=True)
#         .Next(this.check_approve)
#     )
#
#     send_acknowledgement = (
#         flow.Function(this.send_hello_world_request)
#             .Next(this.end)
#     )
#
#     end = flow.End()
