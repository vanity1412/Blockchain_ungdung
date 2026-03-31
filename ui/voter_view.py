"""Voter view for casting votes and viewing results"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QMessageBox, QGroupBox, QTextEdit, QHeaderView)
from PySide6.QtCore import Qt, Signal
from models.voter import Voter
from services.voting_service import VotingService
from services.election_service import ElectionService
from utils.constants import ElectionState

class VoterView(QWidget):
    """View for voters to cast votes"""
    
    logout_signal = Signal()
    
    def __init__(self, voter: Voter, voting_service: VotingService, 
                 election_service: ElectionService):
        super().__init__()
        self.voter = voter
        self.voting_service = voting_service
        self.election_service = election_service
        self.selected_proposal_id = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Header
        header = QLabel(f"👤 Xin chào, {self.voter.full_name}")
        header.setObjectName("subtitleLabel")
        layout.addWidget(header)
        
        # Voter info
        info_group = QGroupBox("Thông tin cử tri")
        info_layout = QVBoxLayout()
        info_layout.addWidget(QLabel(f"Mã cử tri: {self.voter.id}"))
        info_layout.addWidget(QLabel(f"Quyền biểu quyết: {self.voter.weight}"))
        status = "✅ Đã bỏ phiếu" if self.voter.voted else "⏳ Chưa bỏ phiếu"
        info_layout.addWidget(QLabel(f"Trạng thái: {status}"))
        verified = "✅ Đã xác thực" if self.voter.verified else "⚠️ Chưa xác thực"
        info_layout.addWidget(QLabel(f"Xác thực: {verified}"))
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Proposals table
        proposals_group = QGroupBox("Danh sách ứng viên")
        proposals_layout = QVBoxLayout()
        
        self.proposals_table = QTableWidget()
        self.proposals_table.setColumnCount(3)
        self.proposals_table.setHorizontalHeaderLabels(["ID", "Ứng viên", "Mô tả"])
        self.proposals_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.proposals_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.proposals_table.setSelectionMode(QTableWidget.SingleSelection)
        self.proposals_table.itemSelectionChanged.connect(self.on_proposal_selected)
        proposals_layout.addWidget(self.proposals_table)
        
        proposals_group.setLayout(proposals_layout)
        layout.addWidget(proposals_group)
        
        # Vote button
        button_layout = QHBoxLayout()
        self.vote_btn = QPushButton("🗳️ Bỏ phiếu")
        self.vote_btn.setObjectName("successButton")
        self.vote_btn.clicked.connect(self.cast_vote)
        self.vote_btn.setEnabled(False)
        
        self.status_btn = QPushButton("📊 Xem trạng thái phiếu")
        self.status_btn.clicked.connect(self.view_vote_status)
        
        self.results_btn = QPushButton("📈 Xem kết quả")
        self.results_btn.clicked.connect(self.view_results)
        
        logout_btn = QPushButton("🚪 Đăng xuất")
        logout_btn.setObjectName("dangerButton")
        logout_btn.clicked.connect(self.logout_signal.emit)
        
        button_layout.addWidget(self.vote_btn)
        button_layout.addWidget(self.status_btn)
        button_layout.addWidget(self.results_btn)
        button_layout.addStretch()
        button_layout.addWidget(logout_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.load_proposals()
    
    def load_proposals(self):
        """Load proposals into table"""
        proposals = self.voting_service.db_manager.get_all_proposals()
        self.proposals_table.setRowCount(len(proposals))
        
        for row, proposal in enumerate(proposals):
            self.proposals_table.setItem(row, 0, QTableWidgetItem(str(proposal.id)))
            self.proposals_table.setItem(row, 1, QTableWidgetItem(proposal.candidate_name))
            self.proposals_table.setItem(row, 2, QTableWidgetItem(proposal.description))
    
    def on_proposal_selected(self):
        """Handle proposal selection"""
        selected_rows = self.proposals_table.selectedItems()
        if selected_rows and not self.voter.voted:
            self.selected_proposal_id = int(selected_rows[0].text())
            self.vote_btn.setEnabled(True)
        else:
            self.vote_btn.setEnabled(False)
    
    def cast_vote(self):
        """Cast vote for selected proposal"""
        if not self.selected_proposal_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn ứng viên")
            return
        
        election = self.election_service.get_current_election()
        if not election:
            QMessageBox.warning(self, "Lỗi", "Không có cuộc bầu cử nào đang diễn ra")
            return
        
        # Confirm vote
        reply = QMessageBox.question(
            self, "Xác nhận",
            f"Bạn có chắc muốn bỏ phiếu cho ứng viên ID {self.selected_proposal_id}?\n"
            "Hành động này không thể hoàn tác!",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, message = self.voting_service.cast_vote(
                self.voter, self.selected_proposal_id, election
            )
            
            if success:
                QMessageBox.information(self, "Thành công", message)
                self.voter = self.voting_service.db_manager.get_voter_by_id(self.voter.id)
                self.vote_btn.setEnabled(False)
                self.init_ui()  # Refresh UI
            else:
                QMessageBox.warning(self, "Lỗi", message)
    
    def view_vote_status(self):
        """View voter's vote status on blockchain"""
        status = self.voting_service.get_voter_vote_status(self.voter)
        
        if status:
            msg = f"""
📦 Block Index: {status['block_index']}
⏰ Timestamp: {status['timestamp']}
🎯 Ứng viên: {status['proposal'].candidate_name if status['proposal'] else 'N/A'}
🔐 Chữ ký: {status['signature'][:50]}...
#️⃣ Hash: {status['hash'][:50]}...

✅ Phiếu của bạn đã được ghi vào blockchain!
            """
            QMessageBox.information(self, "Trạng thái phiếu bầu", msg)
        else:
            QMessageBox.information(self, "Trạng thái phiếu bầu", 
                                   "Bạn chưa bỏ phiếu hoặc phiếu chưa được ghi nhận")
    
    def view_results(self):
        """View election results"""
        election = self.election_service.get_current_election()
        if not election:
            QMessageBox.warning(self, "Lỗi", "Không có cuộc bầu cử nào")
            return
        
        if election.state != ElectionState.DONE:
            QMessageBox.information(self, "Thông báo", 
                                   "Kết quả chưa được công bố")
            return
        
        proposals = self.voting_service.db_manager.get_all_proposals()
        proposals.sort(key=lambda p: p.vote_count, reverse=True)
        
        result_text = "📊 KẾT QUẢ BẦU CỬ\n\n"
        for i, proposal in enumerate(proposals, 1):
            result_text += f"{i}. {proposal.candidate_name}: {proposal.vote_count} phiếu\n"
        
        if election.winner_id:
            winner = next((p for p in proposals if p.id == election.winner_id), None)
            if winner:
                result_text += f"\n🏆 Người chiến thắng: {winner.candidate_name}"
        
        QMessageBox.information(self, "Kết quả bầu cử", result_text)
